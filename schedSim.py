import argparse
import Queue

class Job:

    jobNum = None
    startTime = -1
    finishTime = -1
    remainingCycles = -1
    pauseCycles = -1

    def __init__(self, runTime, arrivalTime, lineNum):
        self.runTime = runTime
        self.arrivalTime = arrivalTime
        self.lineNum = lineNum
        self.remainingCycles = self.runTime

    def setJobNum(self, jobNum):
        self.jobNum = jobNum

    def setStartTime(self, startTime):
        self.startTime = startTime
        self.pauseCycles = 0

    def setFinishTime(self, finishTime):
        self.finishTime = finishTime

    def getWT(self):
        return self.startTime - self.arrivalTime + self.pauseCycles

    def getTAT(self):
        return self.finishTime - self.arrivalTime

    def __str__(self):
        return "Job " + str(self.jobNum) + "- " + "run:" + str(self.runTime) + \
               " arrive:" + str(self.arrivalTime) + " line:" + str(self.lineNum) + \
               " remaining:" + str(self.remainingCycles)

def printOutput(finished):
    totalTAT = 0
    totalWT = 0
    for jobNum, job in enumerate(finished):
        turnaround = job.getTAT()
        wait = job.getWT()
        print "Job %3d" % jobNum + " -- Turnaround %3.2f" % turnaround + " Wait %3.2f" % wait
        totalTAT += turnaround
        totalWT += wait
    print "Average -- Turnaround %3.2f" % (totalTAT / float(len(finished))) + " Wait %3.2f" % (totalWT / float(len(finished)))

def schedSim():
    # Parse Arguments
    parser = argparse.ArgumentParser(description="A process scheduler simulator")
    parser.add_argument("jobsFilePath", help="jobs file")
    parser.add_argument("-p", help="scheduling algorithm")
    parser.add_argument("-q", help="quantam time", type=int)
    args = parser.parse_args()
    algorithm = args.p
    quantam = args.q

    # Open jobs file
    with open(args.jobsFilePath, 'r') as jobsFile:
        jobs = []
        totalRunTime = 0;
        # Parse file and store into Job class
        for lineNum, line in enumerate(jobsFile, 1):
            jobSplit = line.split(" ")
            runTime = int(jobSplit[0])
            arrivalTime = int(jobSplit[1])
            jobs.append(Job(runTime, arrivalTime, lineNum))
            totalRunTime += runTime

        # Sort jobs based on arrival, then lineNum
        jobs.sort(key=lambda job: (job.arrivalTime, job.jobNum))
        for num, job in enumerate(jobs):
            job.setJobNum(num)
            print job.__str__()

        running = None
        finished = []
        if algorithm == "FIFO":
            queue = Queue.Queue()
            for cycle in range(totalRunTime):
                for job in jobs:
                    if job.arrivalTime == cycle:
                        queue.put(job)
                if running is None:
                    running = queue.get();
                    running.setStartTime(cycle)
                if running is not None:
                    running.remainingCycles -= 1
                print "Cycle: " + str(cycle) + " Job: " + str(running.jobNum)
                if running.remainingCycles == 0:
                    running.setFinishTime(cycle+1)
                    finished.append(running)
                    running = None
            printOutput(finished)

        elif algorithm == "SRJN":
            print "SRJN"
            queuedJobs = []
            for cycle in range(totalRunTime):
                for job in jobs:
                    if job.arrivalTime == cycle:
                        queuedJobs.append(job)
                if len(queuedJobs) > 0:
                    # find job with shortest remaining time. If tie, take job with lower line number
                    queuedJobs.sort(key=lambda qJob: (qJob.remainingCycles, qJob.jobNum))
                    # set running to job with shortest remaining time
                    running = queuedJobs[0]
                    if running.startTime < 0:
                        running.setStartTime(cycle)
                    for queuedJob in queuedJobs[1:]:
                        if queuedJob.pauseCycles >= 0:
                            queuedJob.pauseCycles += 1
                if running is not None:
                    print "Cycle: " + str(cycle) + " Job: " + str(running.jobNum)
                    running.remainingCycles -= 1;
                    if running.remainingCycles == 0:
                        running.setFinishTime(cycle+1)
                        queuedJobs.remove(running)
                        finished.append(running)
            finished.sort(key=lambda x: (x.jobNum))
            printOutput(finished)






if __name__ == '__main__':
    schedSim()