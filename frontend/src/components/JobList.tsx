"use client";

import { useEffect, useState } from "react";
import JobCard from "./JobCard";
import { Job } from "@/types/job";

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/jobs?limit=30&offset=0`)
      .then((res) => res.json())
      .then((data) => setJobs(data));
  }, []);

  return (
    <div className="space-y-4">
      {jobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
