import { Job } from "@/types/job";

type Props = {
  job: Job;
};

export default function JobCard({ job }: Props) {
  return (
  <div className="bg-white p-6 border border-gray-200 rounded-2xl shadow-md hover:shadow-xl transition-shadow duration-300">
    <div className="flex items-center justify-between">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">{job.title}</h2>
        <p className="text-sm text-gray-500">{job.company} · {job.locations}</p>
      </div>
      {job.logo && (
        <img
          src={job.logo}
          alt={`${job.company} logo`}
          className="w-12 h-12 object-contain rounded"
        />
      )}
    </div>

    {job.tags && (
      <p className="mt-3 text-sm text-gray-600">
        <span className="font-medium text-gray-700">Stack:</span> {job.tags}
      </p>
    )}

    {job.salary_from && job.salary_to && (
      <p className="mt-2 text-sm text-green-600 font-medium">
        💰 {job.salary_from} - {job.salary_to} {job.currency}
      </p>
    )}

    <a
      href={job.link}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-block mt-4 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
    >
      Voir l'offre →
    </a>
  </div>
);

}
