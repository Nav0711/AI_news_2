import { X } from "lucide-react";

interface VideoPlayerProps {
  videoUrl: string;
  onClose: () => void;
}

export default function VideoPlayer({ videoUrl, onClose }: VideoPlayerProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-sm aspect-[9/16] bg-black rounded-xl overflow-hidden shadow-2xl border border-border">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Video Element */}
        <video
          src={videoUrl}
          controls
          autoPlay
          className="w-full h-full object-cover"
        />
      </div>
    </div>
  );
}
