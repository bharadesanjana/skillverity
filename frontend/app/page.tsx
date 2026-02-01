import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="px-6 h-16 flex items-center border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="flex items-center gap-2 font-bold text-xl text-primary">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
            SV
          </div>
          SkillVerity
        </div>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
            Features
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
            Pricing
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
            About
          </Link>
        </nav>
        <div className="ml-4">
          <Link href="/login">
            <Button size="sm">Login</Button>
          </Link>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-24 md:py-32 lg:py-48 px-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/20 via-background to-background">
          <div className="container mx-auto flex flex-col items-center text-center space-y-4">
            <div className="px-3 py-1 rounded-full border border-primary/20 bg-primary/10 text-primary text-sm font-medium mb-4">
              Enterprise Grade Career Acceleration
            </div>
            <h1 className="text-4xl font-bold tracking-tighter sm:text-6xl xl:text-7xl/none bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
              Validate Your Skills. <br /> Accelerate Your Career.
            </h1>
            <p className="max-w-[700px] text-gray-400 md:text-xl">
              AI-driven/powered roadmaps, authoritative sourcing, and rigorous validation for the modern professional.
            </p>
            <div className="flex flex-col gap-2 min-[400px]:flex-row pt-4">
              <Link href="/register">
                <Button size="lg" className="h-12 px-8 text-base">
                  Start Your Journey
                </Button>
              </Link>
              <Link href="/login">
                <Button size="lg" variant="outline" className="h-12 px-8 text-base">
                  View Demo
                </Button>
              </Link>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 px-6">
          <div className="container mx-auto grid gap-8 px-4 md:grid-cols-3">
            <Card className="bg-card/50 border-primary/10">
              <CardHeader>
                <CardTitle>AI Roadmaps</CardTitle>
                <CardDescription>Personalized Learning Paths</CardDescription>
              </CardHeader>
              <CardContent>
                Dynamic career roadmaps adapted to your timeline and goals, powered by vector-search RAG.
              </CardContent>
            </Card>
            <Card className="bg-card/50 border-primary/10">
              <CardHeader>
                <CardTitle>Skill Validation</CardTitle>
                <CardDescription>Rigorous Quizzes</CardDescription>
              </CardHeader>
              <CardContent>
                Validation logic that ensures you truly know the material before moving forward.
              </CardContent>
            </Card>
            <Card className="bg-card/50 border-primary/10">
              <CardHeader>
                <CardTitle>Recruiter Ready</CardTitle>
                <CardDescription>Verified Summaries</CardDescription>
              </CardHeader>
              <CardContent>
                Generate verified, recruiter-facing summaries that prove your competency.
              </CardContent>
            </Card>
          </div>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-6 border-t border-border">
        <p className="text-xs text-muted-foreground">© 2026 SkillVerity Inc. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4 text-muted-foreground" href="#">
            Terms of Service
          </Link>
          <Link className="text-xs hover:underline underline-offset-4 text-muted-foreground" href="#">
            Privacy
          </Link>
        </nav>
      </footer>
    </div>
  );
}
