import { Job } from "@/types/job";

type Props = {
  job: Job;
};

export default function JobCard({ job }: Props) {
  return (
    <div className="bg-white p-6 border border-gray-200 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h2 className="text-xl font-semibold text-gray-900 tracking-tight">
            {job.title}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            {job.company} ·{" "}
            <span className="text-gray-400">{job.locations}</span>
          </p>
        </div>
        {job.logo && (
          <img
            src={job.logo}
            alt={`${job.company} logo`}
            className="w-14 h-14 object-contain rounded-md border border-gray-100 bg-gray-50 p-1"
          />
        )}
      </div>

      {job.tags && (
        <p className="mt-4 text-sm text-gray-700">
          <span className="font-medium text-gray-800">Stack:</span>{" "}
          <span className="text-gray-600">{job.tags}</span>
        </p>
      )}

      {job.salary_from && job.salary_to && (
        <p className="mt-2 text-sm text-green-600 font-semibold">
          💰 {job.salary_from} – {job.salary_to} {job.currency}
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
