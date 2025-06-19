import JobList from "@/components/JobList";

export default function Home() {
  return (
    <main className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Offres d’emploi Dev</h1>
      <JobList />
    </main>
  );
}
