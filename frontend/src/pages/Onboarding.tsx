import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/lib/auth";
import { ArrowRight, Briefcase, GraduationCap, LineChart, Cpu } from "lucide-react";
import { toast } from "sonner";

const PERSONAS = [
  {
    id: "investor",
    title: "Mutual Fund/Stock Investor",
    description: "Portfolio-relevant stories, market movements, and corporate earnings.",
    icon: <LineChart className="w-8 h-8 text-secondary" />,
    interests: ["stocks", "macro", "corporate"]
  },
  {
    id: "founder",
    title: "Startup Founder",
    description: "Funding news, competitor moves, and venture capital insights.",
    icon: <Briefcase className="w-8 h-8 text-primary" />,
    interests: ["startup", "corporate", "macro"]
  },
  {
    id: "student",
    title: "Student & Learner",
    description: "Explainer-first content, economy basics, and career trends.",
    icon: <GraduationCap className="w-8 h-8 text-yellow-500" />,
    interests: ["crypto", "macro", "startup"]
  },
  {
    id: "tech_exec",
    title: "Tech Executive",
    description: "Deep tech, M&A, crypto, and enterprise strategy.",
    icon: <Cpu className="w-8 h-8 text-purple-500" />,
    interests: ["startup", "corporate", "crypto", "stocks"]
  }
];

export default function Onboarding() {
  const [selectedPersona, setSelectedPersona] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { updateProfile } = useAuth();
  const navigate = useNavigate();

  const handleComplete = async () => {
    if (!selectedPersona) return;
    
    setLoading(true);
    const persona = PERSONAS.find(p => p.id === selectedPersona);
    
    try {
      await updateProfile({
        profile_type: persona!.id,
        interests: persona!.interests
      });
      toast.success("Profile personalized!");
      navigate("/dashboard");
    } catch (error: any) {
      toast.error(error.message || "Failed to update profile.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden flex flex-col justify-center transition-colors duration-300">
      {/* Background decoration */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[60%] h-[60%] rounded-full bg-primary/10 blur-[120px]" />
        <div className="absolute bottom-0 left-0 w-[60%] h-[60%] rounded-full bg-secondary/10 blur-[120px]" />
      </div>

      <div className="max-w-4xl mx-auto w-full z-10 animate-fade-in relative">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold tracking-tight font-display sm:text-5xl mb-4">
            Personalize Your <span className="text-primary italic">Newsroom</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            My ET is not just a filtered feed. It's a fundamentally different news experience based on who you are.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {PERSONAS.map((persona) => (
            <button
              key={persona.id}
              onClick={() => setSelectedPersona(persona.id)}
              className={`text-left p-6 rounded-2xl border transition-all duration-300 relative overflow-hidden group ${
                selectedPersona === persona.id
                  ? "bg-primary/5 border-primary shadow-lg shadow-primary/10"
                  : "bg-card border-border hover:border-primary/40 hover:bg-muted/50"
              }`}
            >
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-background rounded-xl border border-border">
                  {persona.icon}
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-2">{persona.title}</h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {persona.description}
                  </p>
                </div>
              </div>
              {selectedPersona === persona.id && (
                <div className="absolute top-4 right-4">
                  <div className="w-3 h-3 bg-primary rounded-full animate-pulse shadow-[0_0_10px_rgba(var(--primary),0.8)]" />
                </div>
              )}
            </button>
          ))}
        </div>

        <div className="flex justify-center flex-col items-center space-y-4">
          <button
            onClick={handleComplete}
            disabled={!selectedPersona || loading}
            className={`flex items-center space-x-2 px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ${
              selectedPersona 
                ? "bg-primary text-primary-foreground shadow-lg hover:shadow-primary/40 hover:-translate-y-1 active:scale-95" 
                : "bg-muted text-muted-foreground border border-border cursor-not-allowed"
            }`}
          >
            <span>{loading ? "Personalizing Engine..." : "Enter My ET"}</span>
            {!loading && <ArrowRight className="w-5 h-5" />}
          </button>
          <p className="text-sm text-muted-foreground">You can always adjust your interests later.</p>
        </div>
      </div>
    </div>
  );
}
