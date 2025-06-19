import { Job } from "@/types/job";

type Props = {
  job: Job;
};

export default function JobCard({ job }: Props) {
  return (
    <div className="bg-white p-4 border rounded shadow">
      <h2 className="text-xl font-semibold">{job.title}</h2>
      <p className="text-sm text-gray-600">{job.company} – {job.locations}</p>
      {job.tags && <p className="text-sm text-gray-800 mt-1">{job.tags}</p>}
      {job.salary_from && job.salary_to && (
        <p className="text-sm mt-1 text-green-700">
          💰 {job.salary_from} - {job.salary_to} {job.currency}
        </p>
      )}
      <a
        href={job.link}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 text-sm underline inline-block mt-2"
      >
        Voir l'offre
      </a>
    </div>
  );
}
