import { useAuth } from "@/lib/auth";
import { Link, useNavigate } from "react-router-dom";
import { User, LogOut, Settings, Newspaper, ArrowLeft } from "lucide-react";

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-background text-foreground animate-fade-in font-sans">
      <nav className="flex items-center px-6 py-4 border-b border-border bg-card/95 backdrop-blur-sm sticky top-0 z-50">
        <Link to="/dashboard" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mr-6">
          <ArrowLeft className="w-5 h-5" />
          <span className="font-medium text-sm">Dashboard</span>
        </Link>
        <h1 className="font-display text-xl tracking-tight">
          My<span className="text-primary">Profile</span>
        </h1>
      </nav>

      <main className="max-w-2xl mx-auto py-12 px-6">
        <div className="flex items-center gap-6 mb-10">
          <div className="w-24 h-24 rounded-full bg-primary/10 border-2 border-primary/20 flex items-center justify-center">
            <User className="w-10 h-10 text-primary" />
          </div>
          <div>
            <h2 className="text-3xl font-display font-medium tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
              {user.email.split('@')[0]}
            </h2>
            <p className="text-muted-foreground font-mono-jet text-sm mt-1">{user.email}</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm hover:border-primary/30 transition-colors">
            <div className="flex items-center gap-2 mb-4 text-primary">
              <Settings className="w-5 h-5" />
              <h3 className="font-medium text-foreground">Account Details</h3>
            </div>
            <div className="space-y-4">
              <div>
                <p className="text-xs font-mono-jet text-muted-foreground tracking-wider mb-1">PROFILE TYPE</p>
                <p className="capitalize font-medium">{user.profile_type?.replace('_', ' ') || 'Standard Reader'}</p>
              </div>
              <div>
                <p className="text-xs font-mono-jet text-muted-foreground tracking-wider mb-2">PERSONALIZED INTERESTS</p>
                <div className="flex flex-wrap gap-2">
                  {user.interests.map(interest => (
                    <span key={interest} className="px-3 py-1 bg-secondary/10 text-secondary border border-secondary/20 rounded-md text-sm font-medium">
                      {interest}
                    </span>
                  ))}
                  {user.interests.length === 0 && (
                    <span className="text-muted-foreground text-sm">No special interests defined.</span>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-6 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4 hover:border-border/80 transition-colors">
            <div className="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
              <div className="w-12 h-12 rounded-full bg-muted/50 flex flex-shrink-0 items-center justify-center">
                <Newspaper className="w-6 h-6 text-muted-foreground" />
              </div>
              <div>
                <h3 className="font-medium">Modify Preferences</h3>
                <p className="text-sm text-muted-foreground">Change your default topics and briefing styles.</p>
              </div>
            </div>
            <Link to="/onboarding" className="w-full sm:w-auto px-5 py-2 rounded-lg bg-secondary text-secondary-foreground text-sm font-medium hover:opacity-90 transition-opacity text-center shadow-md">
              Edit Feed
            </Link>
          </div>

          <button 
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-6 py-4 rounded-xl border border-destructive/30 text-destructive bg-destructive/5 hover:bg-destructive/10 transition-colors font-medium mt-12"
          >
            <LogOut className="w-5 h-5" />
            Sign out of MyET
          </button>
        </div>
      </main>
    </div>
  );
}
