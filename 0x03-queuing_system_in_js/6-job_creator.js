import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '1234567890',
  message: 'This is a notification message',
};

queue.create('push_notification_code', jobData)
  .save((err, job) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    } else {
      console.error('Error creating job:', err);
    }
  });

queue.on('job complete', (id) => {
  console.log(`Notification job ${id} completed`);
});

queue.on('job failed', (id, err) => {
  console.error(`Notification job ${id} failed:`, err);
});
