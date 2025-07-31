"use client";

import { useEffect, useState } from "react";
import JobCard from "./JobCard";
import { Job } from "@/types/job";

export default function JobList() {
  const NEXT_PUBLIC_API_URL = "http://0.0.0.0:8000/";

  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}`
)
      .then((res) => res.json())
      .then((data) => setJobs(data));
  }, []);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {jobs.map((job) => (
      <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
