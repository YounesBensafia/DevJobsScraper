import { Job } from "@/types/job";
import Image from "next/image";
import React from "react";
import { useState } from "react";

type Props = {
  job: Job;
};

export default function JobCard({ job }: Props) {
  const [showAll, setShowAll] = useState(false);
  const [logoError, setLogoError] = useState(false);
  const locationsArray = job.locations.split(",");

  const displayedLocations = showAll
    ? job.locations
    : locationsArray.length > 4
    ? locationsArray.slice(0, 3).join(",") + ", "
    : job.locations;
  return (
    <div className="bg-white border border-gray-200 rounded-3xl shadow-sm hover:shadow-lg transition-all duration-300 p-6 space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h2 className="text-2xl font-semibold text-gray-900">{job.title}</h2>
          <p className="mt-1 text-sm text-gray-500">
            {job.company} ·{" "}
            <span className="text-gray-400 break-words whitespace-normal">
              {displayedLocations}
              {locationsArray.length > 4 && !showAll && (
                <button
                  onClick={() => setShowAll(true)}
                  className="text-blue-500 hover:underline ml-1"
                >
                  Voir plus
                </button>
              )}
              {locationsArray.length > 4 && showAll && (
                <button
                  onClick={() => setShowAll(false)}
                  className="text-blue-500 hover:underline ml-1"
                >
                  Voir moins
                </button>
              )}
            </span>
          </p>
        </div>

        {/* Logo or fallback SVG */}
        <div className="w-16 h-16 flex items-center justify-center bg-gray-50 border border-gray-100 rounded-xl p-2">
          {!logoError && job.logo ? (
            <img
              src={job.logo}
              alt={`${job.company} logo`}
              onError={() => setLogoError(true)}
              className="w-full h-full object-contain"
            />
          ) : (
            <Image
              src="/world.svg"
              alt="world"
              width={64}
              height={64}
              className="w-full h-full object-contain"
            />
          )}
        </div>
      </div>

      {job.tags && (
        <p className="mt-4 text-sm text-gray-700">
          <span className="font-medium text-gray-800">Stack:</span>{" "}
          <span className="text-gray-600">{job.tags}</span>
        </p>
      )}

      {job.salary_from && job.salary_to && (
        <p className="mt-2 text-sm text-green-600 font-semibold">
          💰 {Number(job.salary_from).toLocaleString()} –{" "}
          {Number(job.salary_to).toLocaleString()} {job.currency}
        </p>
      )}

      <div className="mt-5 flex items-center justify-between">
        <a
          href={job.link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-all"
        >
          Voir l'offre →
        </a>
        {job.time && (
          <p className="text-xs text-gray-400 whitespace-nowrap">
            🗓️ {job.time}
          </p>
        )}
      </div>
    </div>
  );
}
