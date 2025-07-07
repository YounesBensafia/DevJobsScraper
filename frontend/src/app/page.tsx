import JobList from "@/components/JobList";
import Filter from "@/components/Filter";

export default function Home() {
  return (
    <main className="p-4">
      <div className="relative bg-black py-16 px-6 sm:px-12 lg:px-24 mb-8 border-3 rounded-2xl shadow-lg">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white mb-6">
            Discover Remote{" "}
            <span className="text-blue-600 dark:text-blue-400">Developer</span>{" "}
            Opportunities
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Find your next career move — wherever you are. Browse fully remote
            jobs in frontend, backend, and full-stack development.
          </p>
        </div>
      </div>

      {/* <Filter /> */}
      <JobList />
    </main>
  );
}
