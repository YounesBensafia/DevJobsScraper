"use client";
import JobList from "@/components/JobList";
import Filter from "@/components/Filter";
import SplitText from "@/components/react_bits/SplitText";

export default function Home() {
  const handleAnimationComplete = () => {
    console.log("All letters have animated!");
  };
  return (
    <main className="pl-4 pr-4">
      <SplitText
        text="Hello in JobHunter!"
        className="text-3xl italic text-black w-full text-center font-bold mb-8 mt-8 md:text-8xl"
        delay={100}
        duration={0.6}
        ease="power3.out"
        splitType="chars"
        from={{ opacity: 0, y: 40 }}
        to={{ opacity: 1, y: 0 }}
        rootMargin="-100px"
        textAlign="center"
        threshold={0.1}
        
        onLetterAnimationComplete={handleAnimationComplete}
      />
      <JobList />
    </main>
  );
}
