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
    <div
      className="bg-white border-3 border-black rounded-4xl shadow-sm hover:shadow-lg transition-all duration-300 p-6 space-y-4"
      style={{
        backgroundImage: `url("/card_background.svg")`,
        backgroundAttachment: "fixed",
        backgroundColor: "rgba(255, 255, 255, 0.6)", // Adds a semi-transparent white background
        backgroundBlendMode: "overlay", // Blends the background image with the background color
      }}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h2 className="text-2xl font-semibold text-gray-900">{job.title}</h2>
          <p className="mt-1 text-xl text-[#6D65C6] font-bold ">
            {job.company}
          </p>
          <span className="text-gray-400 font-bold text-[15px] break-words whitespace-normal">
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
        </div>

        <div className="w-16 h-full rounded-xl flex items-center justify-center bg-[#6D65C6] border border-black p-2">
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
        <p className="mt-4 text-xl text-gray-700 ">
          <span className="text-amber-400 font-bold">{job.tags}</span>
        </p>
      )}

      {job.salary_from && job.salary_to && (
        <p className="mt-2 text-xl text-[#09A372] font-semibold">
          {job.currency}
          {Number(job.salary_from).toLocaleString()} - {job.currency}
          {Number(job.salary_to).toLocaleString()}
        </p>
      )}

      <div className="mt-5 flex items-center justify-between ">
        <a
          href={job.link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-md text-white bg-[#5644E6] border-2 border-black hover:bg-blue-300 hover:text-black px-4 py-2 ring-1 shadow-orange-400 rounded-full font-bold transition-all"
        >
          Voir l'offre →
        </a>
        {job.time && (
          <p className="text-[20px] font-bold text-[#5644E6] whitespace-nowrap">
            🗓️ {job.time}
          </p>
        )}
      </div>
    </div>
  );
}
