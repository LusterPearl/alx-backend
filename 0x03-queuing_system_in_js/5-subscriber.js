import redis from 'redis';

const subscriber = redis.createClient();

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
  subscriber.subscribe('holberton school channel');
});

subscriber.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

subscriber.on('message', (channel, message) => {
  console.log(`Message received on channel ${channel}: ${message}`);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe('holberton school channel');
    subscriber.quit();
  }
});
