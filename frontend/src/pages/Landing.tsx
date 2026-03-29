import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/lib/auth";
import { useTheme } from "@/components/ThemeProvider";
import { Moon, Sun, ChevronRight, Globe, Zap, Languages, Shield } from "lucide-react";

export default function Landing() {
  const { theme, setTheme } = useTheme();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleCTA = () => {
    if (isAuthenticated) {
      navigate("/dashboard");
    } else {
      navigate("/login");
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans transition-colors duration-300">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Globe className="w-6 h-6 text-primary" />
          <h1 className="font-display text-2xl tracking-tight">
            My<span className="text-primary">ET</span>
            <span className="inline-block w-2 h-2 rounded-full bg-secondary ml-1 animate-pulse" />
          </h1>
        </div>
        
        <div className="flex items-center gap-4">
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 rounded-full bg-muted text-muted-foreground hover:bg-muted/80 transition-colors"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          
          {isAuthenticated ? (
            <Link to="/dashboard" className="text-sm font-medium hover:text-primary transition-colors">
              Dashboard
            </Link>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className="text-sm font-medium hover:text-primary transition-colors">
                Sign In
              </Link>
              <Link to="/register" className="text-sm font-medium bg-primary text-primary-foreground px-4 py-2 rounded-md shadow-lg shadow-primary/20 hover:opacity-90 transition-opacity">
                Get Started
              </Link>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center pt-20 pb-16 px-6 text-center">
        <div className="absolute inset-0 -z-10 h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]">
          <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary opacity-20 blur-[100px]"></div>
          <div className="absolute right-0 bottom-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-secondary opacity-20 blur-[100px]"></div>
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-8 animate-fade-in">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
          The Future of Business News
        </div>

        <h2 className="text-5xl md:text-7xl font-display font-bold tracking-tight max-w-4xl leading-tight mb-6 animate-slide-in-right">
          Contextual AI Intelligence for <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">Indian Markets</span>
        </h2>

        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 text-balance">
          Real-time vernacular translations, personalized insights, and cultural adaptations of financial events delivered directly to your dashboard.
        </p>

        <button 
          onClick={handleCTA}
          className="group flex items-center gap-2 bg-foreground text-background px-8 py-4 rounded-lg font-medium text-lg hover:bg-foreground/90 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1"
        >
          {isAuthenticated ? "Go to Dashboard" : "Experience MyET AI"}
          <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </button>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mt-24">
          <div className="flex flex-col items-center text-center p-6 rounded-2xl bg-card border border-border shadow-sm hover:border-primary/50 transition-colors">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-bold text-lg mb-2">Real-time Insights</h3>
            <p className="text-muted-foreground text-sm">Lightning fast data aggregation matching current market pulses and live tickers.</p>
          </div>
          
          <div className="flex flex-col items-center text-center p-6 rounded-2xl bg-card border border-border shadow-sm hover:border-secondary/50 transition-colors">
            <div className="w-12 h-12 rounded-full bg-secondary/10 flex items-center justify-center mb-4">
              <Languages className="w-6 h-6 text-secondary" />
            </div>
            <h3 className="font-bold text-lg mb-2">Vernacular Engine</h3>
            <p className="text-muted-foreground text-sm">Culturally adapted explanations of English business news into Hindi, Tamil and more.</p>
          </div>

          <div className="flex flex-col items-center text-center p-6 rounded-2xl bg-card border border-border shadow-sm hover:border-primary/50 transition-colors">
            <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-foreground" />
            </div>
            <h3 className="font-bold text-lg mb-2">Personalized Briefings</h3>
            <p className="text-muted-foreground text-sm">Hyper-targeted story arcs customized to the interests you set in your profile.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
