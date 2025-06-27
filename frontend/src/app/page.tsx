import JobList from "@/components/JobList";
import Filter from "@/components/Filter"; 

export default function Home() {
  return (
    <main className="p-6">
      {/* <h1 className="text-3xl font-bold mb-6 flex justify-center">Offres d’emploi Dev</h1> */}
      {/* <Filter /> */}
      <JobList />
    </main>
  );
}
