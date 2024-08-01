import { expect } from "chai";
import kue from "kue";
import createPushNotificationsJobs from "./8-job";

describe("createPushNotificationsJobs", () => {
  const queue = kue.createQueue();

  before(() => {
    kue.Job.testMode.enter();
  });

  afterEach(() => {
    kue.Job.testMode.clear();
  });

  after(() => {
    kue.Job.testMode.exit();
  });

  it("should throw an error if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(
      "Jobs is not an array",
    );
  });

  it("should create jobs when given an array of job data", () => {
    const jobs = [
      {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
      },
      {
        phoneNumber: "4153518781",
        message: "This is the code 4562 to verify your account",
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    const createdJobs = kue.Job.testMode.jobs;
    expect(createdJobs.length).to.equal(2);
    expect(createdJobs[0].type).to.equal("push_notification_code_3");
    expect(createdJobs[0].data).to.deep.equal(jobs[0]);
    expect(createdJobs[1].type).to.equal("push_notification_code_3");
    expect(createdJobs[1].data).to.deep.equal(jobs[1]);
  });
});
