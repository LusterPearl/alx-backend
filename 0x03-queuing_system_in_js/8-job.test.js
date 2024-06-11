import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => {
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.exit();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  it('display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(null, queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '1234567890', message: 'test message 1' },
      { phoneNumber: '9876543210', message: 'test message 2' }
    ];

    createPushNotificationsJobs(jobs, queue);

    const createdJobs = queue.testMode.jobs;
    expect(createdJobs).to.have.lengthOf(2);
    expect(createdJobs[0].type).to.equal('push_notification_code_3');
    expect(createdJobs[0].data).to.deep.equal(jobs[0]);
    expect(createdJobs[1].type).to.equal('push_notification_code_3');
    expect(createdJobs[1].data).to.deep.equal(jobs[1]);
  });
});
