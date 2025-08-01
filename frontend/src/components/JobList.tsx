"use client";

import { useEffect, useState } from "react";
import JobCard from "./JobCard";
import { Job } from "@/types/job";
import NEXT_PUBLIC_API_URL from "@/config/index";

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);
  console.log("NEXT_PUBLIC_API_URL", NEXT_PUBLIC_API_URL);

  useEffect(() => {
    fetch(`${NEXT_PUBLIC_API_URL}`)
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
