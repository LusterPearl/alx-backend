import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Data
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

// Data access
const getItemById = id => listProducts.find(product => product.id === id);

// Server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

// Products
app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  }));
  res.json(products);
});

// In stock in Redis
const client = redis.createClient();
const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async itemId => {
  const getAsync = promisify(client.get).bind(client);
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock) : 0;
};

// Product detail
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock,
      currentQuantity
    });
  }
});

// Reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    if (currentQuantity >= item.stock) {
      res.json({ status: 'Not enough stock available', itemId });
    } else {
      reserveStockById(itemId, currentQuantity + 1);
      res.json({ status: 'Reservation confirmed', itemId });
    }
  }
});
