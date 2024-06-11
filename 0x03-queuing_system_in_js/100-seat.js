import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();
const reserveSeat = number => {
  client.set('available_seats', number);
};
const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats) : 0;
};

// Kue queue
const queue = kue.createQueue();

// Initialize number of seats and reservation status
reserveSeat(50);
let reservationEnabled = true;

// Server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    queue.create('reserve_seat').save();
    res.json({ status: 'Reservation in process' });
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  const currentAvailableSeats = await getCurrentAvailableSeats();
  if (currentAvailableSeats === 0) {
    reservationEnabled = false;
  } else if (currentAvailableSeats > 0) {
    try {
      reserveSeat(currentAvailableSeats - 1);
    } catch (err) {
      console.error(err);
    }
  }
});

// Process the queue
queue.process('reserve_seat', async (job, done) => {
  const currentAvailableSeats = await getCurrentAvailableSeats();
  if (currentAvailableSeats === 0) {
    done(new Error('Not enough seats available'));
  } else {
    done();
  }
});

queue.on('job complete', (id) => {
  console.log(`Seat reservation job ${id} completed`);
});

queue.on('job failed', (id, err) => {
  console.log(`Seat reservation job ${id} failed: ${err.message}`);
});
