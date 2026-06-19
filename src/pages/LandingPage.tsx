import { Link } from "react-router-dom";
import { useTheme } from "@/contexts/ThemeContext";
import { Button } from "@/components/ui/button";
import {
  Leaf, Wind, Zap, Fuel, Bot, BarChart3, Sun, Moon,
  ArrowRight, Database, Brain, LineChart, CheckCircle2,
  Github, Linkedin, MessageSquare, TrendingUp, ShieldCheck, Target
} from "lucide-react";
import { motion } from "framer-motion";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number = 0) => ({
    opacity: 1, y: 0,
    transition: { delay: i * 0.1, duration: 0.5, ease: [0, 0, 0.2, 1] as const }
  }),
};

const stagger = { visible: { transition: { staggerChildren: 0.1 } } };

function Navbar() {
  const { theme, toggleTheme } = useTheme();
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-border/50 bg-background/80 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
            <Leaf className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="text-lg font-bold tracking-tight">SDMP</span>
        </Link>
        <div className="hidden items-center gap-6 text-sm font-medium text-muted-foreground md:flex">
          <a href="#features" className="transition-colors hover:text-foreground">Features</a>
          <a href="#how-it-works" className="transition-colors hover:text-foreground">How It Works</a>
          <a href="#ai-agent" className="transition-colors hover:text-foreground">AI Agent</a>
          <a href="#tech" className="transition-colors hover:text-foreground">Tech Stack</a>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={toggleTheme} className="rounded-full">
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          <Link to="/login"><Button variant="ghost" size="sm">Login</Button></Link>
          <Link to="/register"><Button size="sm">Get Started</Button></Link>
        </div>
      </div>
    </nav>
  );
}

function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-32 pb-20 lg:pt-40 lg:pb-28">
      <div className="absolute inset-0 gradient-bg opacity-[0.06] dark:opacity-[0.12]" />
      <div className="absolute top-20 -left-32 h-96 w-96 rounded-full bg-primary/10 blur-3xl" />
      <div className="absolute bottom-10 -right-32 h-96 w-96 rounded-full bg-accent/10 blur-3xl" />
      <div className="relative mx-auto grid max-w-7xl gap-12 px-4 sm:px-6 lg:grid-cols-2 lg:items-center lg:px-8">
        <motion.div initial="hidden" animate="visible" variants={stagger} className="space-y-6">
          <motion.div variants={fadeUp} custom={0} className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-xs font-medium text-primary">
            <Leaf className="h-3.5 w-3.5" /> AI & Data Science Mega Project
          </motion.div>
          <motion.h1 variants={fadeUp} custom={1} className="text-4xl font-extrabold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
            Monitor. Analyze. Optimize.{" "}
            <span className="gradient-text">Build a Sustainable Future.</span>
          </motion.h1>
          <motion.p variants={fadeUp} custom={2} className="max-w-lg text-lg text-muted-foreground">
            AI-powered sustainability monitoring platform for smart industries. Track emissions, optimize energy, and get actionable insights.
          </motion.p>
          <motion.div variants={fadeUp} custom={3} className="flex flex-wrap gap-3">
            <Link to="/register">
              <Button size="lg" className="gap-2 px-6">Get Started <ArrowRight className="h-4 w-4" /></Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="px-6">View Dashboard Demo</Button>
            </Link>
          </motion.div>
          <motion.div variants={fadeUp} custom={4} className="flex items-center gap-6 pt-2 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-primary" /> Real-time Monitoring</span>
            <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-primary" /> AI-Powered</span>
          </motion.div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7, delay: 0.3 }}
          className="relative hidden lg:block">
          <div className="rounded-2xl border border-border bg-card p-6 shadow-xl">
            <div className="mb-4 flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-destructive/60" />
              <div className="h-3 w-3 rounded-full bg-warning/60" />
              <div className="h-3 w-3 rounded-full bg-success/60" />
              <span className="ml-2 text-xs text-muted-foreground">SDMP Dashboard</span>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: "Carbon Emissions", value: "2,847 t", icon: Leaf, color: "text-primary" },
                { label: "Air Quality", value: "72 AQI", icon: Wind, color: "text-accent" },
                { label: "Energy Usage", value: "1.2M kWh", icon: Zap, color: "text-warning" },
                { label: "Sustainability", value: "87%", icon: TrendingUp, color: "text-success" },
              ].map((kpi) => (
                <div key={kpi.label} className="rounded-xl border border-border bg-background p-4">
                  <kpi.icon className={`h-5 w-5 ${kpi.color} mb-2`} />
                  <p className="text-xs text-muted-foreground">{kpi.label}</p>
                  <p className="text-xl font-bold">{kpi.value}</p>
                </div>
              ))}
            </div>
            <div className="mt-4 h-28 rounded-lg border border-border bg-muted/50 flex items-end justify-around px-4 pb-3">
              {[40, 65, 50, 80, 60, 75, 55, 90, 70, 85, 68, 72].map((h, i) => (
                <div key={i} className="w-3 rounded-t bg-primary/70" style={{ height: `${h}%` }} />
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

function WhySection() {
  const items = [
    { icon: Leaf, title: "Track Carbon Emissions", desc: "Monitor CO₂, CH₄, and N₂O across all industrial units in real-time." },
    { icon: Wind, title: "Monitor Air Quality", desc: "Track AQI, PM2.5, PM10, and pollutant levels continuously." },
    { icon: Zap, title: "Optimize Energy", desc: "Analyze renewable vs non-renewable energy consumption patterns." },
    { icon: Fuel, title: "Manage Fuel Usage", desc: "Track diesel, petrol, and gas consumption with cost estimation." },
    { icon: Bot, title: "AI Recommendations", desc: "Get intelligent suggestions to improve sustainability scores." },
  ];
  return (
    <section className="py-20 lg:py-28 bg-muted/30">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger} className="text-center mb-14">
          <motion.h2 variants={fadeUp} className="text-3xl font-bold sm:text-4xl">Why <span className="gradient-text">SDMP</span>?</motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-muted-foreground max-w-2xl mx-auto">A comprehensive platform that empowers industries to meet sustainability goals with data-driven decisions.</motion.p>
        </motion.div>
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} variants={stagger} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {items.map((item, i) => (
            <motion.div key={item.title} variants={fadeUp} custom={i}
              className="group rounded-xl border border-border bg-card p-6 text-center transition-all duration-300 hover:shadow-lg hover:-translate-y-1 hover:border-primary/30">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                <item.icon className="h-6 w-6" />
              </div>
              <h3 className="font-semibold mb-1.5 text-sm">{item.title}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  const features = [
    { icon: Leaf, title: "Carbon Emission Monitoring", desc: "Real-time tracking of greenhouse gases with detailed breakdowns by industry unit." },
    { icon: Wind, title: "Air Quality Intelligence", desc: "Continuous AQI monitoring with color-coded alerts and pollutant analysis." },
    { icon: Zap, title: "Energy Management System", desc: "Compare renewable vs non-renewable usage with monthly trend analysis." },
    { icon: Fuel, title: "Fuel Consumption Tracking", desc: "Monitor diesel, petrol, and gas usage with automated cost estimation." },
    { icon: Bot, title: "AI Recommendation Agent", desc: "Chat-based AI advisor for root cause detection and optimization strategies." },
    { icon: BarChart3, title: "Advanced Reports & Analytics", desc: "Export PDF/CSV reports with sustainability performance dashboards." },
  ];
  return (
    <section id="features" className="py-20 lg:py-28 scroll-mt-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger} className="text-center mb-14">
          <motion.h2 variants={fadeUp} className="text-3xl font-bold sm:text-4xl">Core <span className="gradient-text">Features</span></motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-muted-foreground max-w-2xl mx-auto">Everything you need to monitor, analyze, and optimize industrial sustainability performance.</motion.p>
        </motion.div>
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.1 }} variants={stagger} className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f, i) => (
            <motion.div key={f.title} variants={fadeUp} custom={i}
              className="group relative overflow-hidden rounded-xl border border-border bg-card p-7 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 hover:border-primary/30">
              <div className="absolute top-0 right-0 h-24 w-24 rounded-bl-full bg-primary/5 transition-colors group-hover:bg-primary/10" />
              <div className="relative">
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                  <f.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold">{f.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

function HowItWorksSection() {
  const steps = [
    { icon: Database, title: "Collect Environmental Data", desc: "Gather real-time data from sensors, IoT devices, and industrial systems." },
    { icon: Brain, title: "Analyze with AI Models", desc: "Process data using machine learning for pattern detection and predictions." },
    { icon: LineChart, title: "Generate Actionable Insights", desc: "Receive optimized recommendations to improve sustainability performance." },
  ];
  return (
    <section id="how-it-works" className="py-20 lg:py-28 bg-muted/30 scroll-mt-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger} className="text-center mb-16">
          <motion.h2 variants={fadeUp} className="text-3xl font-bold sm:text-4xl">How It <span className="gradient-text">Works</span></motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-muted-foreground max-w-2xl mx-auto">Three simple steps to transform your industry's sustainability performance.</motion.p>
        </motion.div>
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} variants={stagger} className="relative grid gap-8 lg:grid-cols-3">
          <div className="absolute top-16 left-[16%] right-[16%] hidden h-0.5 bg-gradient-to-r from-primary/20 via-primary/40 to-primary/20 lg:block" />
          {steps.map((s, i) => (
            <motion.div key={s.title} variants={fadeUp} custom={i} className="relative text-center">
              <div className="relative z-10 mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border-2 border-primary bg-background text-primary shadow-lg shadow-primary/10">
                <s.icon className="h-7 w-7" />
                <span className="absolute -top-2 -right-2 flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">{i + 1}</span>
              </div>
              <h3 className="mb-2 text-lg font-semibold">{s.title}</h3>
              <p className="mx-auto max-w-xs text-sm text-muted-foreground">{s.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

function AIAgentSection() {
  const bullets = [
    { icon: Target, text: "Root cause detection for environmental anomalies" },
    { icon: TrendingUp, text: "Optimization suggestions for energy & emissions" },
    { icon: LineChart, text: "Impact prediction with confidence scores" },
    { icon: ShieldCheck, text: "Sustainability score improvement tips" },
  ];
  return (
    <section id="ai-agent" className="py-20 lg:py-28 scroll-mt-16">
      <div className="mx-auto grid max-w-7xl gap-12 px-4 sm:px-6 lg:grid-cols-2 lg:items-center lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger}>
          <motion.div variants={fadeUp} className="inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent/5 px-4 py-1.5 text-xs font-medium text-accent mb-4">
            <Bot className="h-3.5 w-3.5" /> AI-Powered
          </motion.div>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl font-bold sm:text-4xl mb-4">Built-in AI <span className="gradient-text">Sustainability Advisor</span></motion.h2>
          <motion.p variants={fadeUp} custom={2} className="text-muted-foreground mb-8">Ask questions, get instant analysis, and receive actionable recommendations from our AI agent trained on sustainability data.</motion.p>
          <motion.div variants={stagger} className="space-y-4">
            {bullets.map((b, i) => (
              <motion.div key={i} variants={fadeUp} custom={i + 3} className="flex items-center gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <b.icon className="h-4 w-4" />
                </div>
                <span className="text-sm">{b.text}</span>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }}
          className="rounded-2xl border border-border bg-card p-5 shadow-lg">
          <div className="mb-3 flex items-center gap-2 border-b border-border pb-3">
            <Bot className="h-5 w-5 text-primary" />
            <span className="text-sm font-semibold">AI Sustainability Advisor</span>
            <span className="ml-auto rounded-full bg-success/10 px-2 py-0.5 text-[10px] font-medium text-success">Online</span>
          </div>
          <div className="space-y-3">
            <div className="ml-auto max-w-[75%] rounded-xl rounded-br-sm bg-primary px-4 py-2.5 text-sm text-primary-foreground">
              How can I reduce carbon emissions in Unit B?
            </div>
            <div className="max-w-[85%] rounded-xl rounded-bl-sm border border-border bg-muted/50 p-4">
              <p className="text-xs font-semibold text-primary mb-2">Recommendation</p>
              <div className="space-y-2 text-xs text-muted-foreground">
                <p><span className="font-medium text-foreground">Problem:</span> Unit B emissions 23% above target</p>
                <p><span className="font-medium text-foreground">Root Cause:</span> Outdated boiler system with low efficiency</p>
                <p><span className="font-medium text-foreground">Action:</span> Upgrade to condensing boiler technology</p>
                <p><span className="font-medium text-foreground">Impact:</span> ~18% emission reduction in 6 months</p>
              </div>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 rounded-lg border border-border bg-background px-3 py-2">
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
            <span className="text-xs text-muted-foreground">Ask about sustainability...</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

function TechStackSection() {
  const groups = [
    { label: "Frontend", items: ["React", "TypeScript", "Tailwind CSS"] },
    { label: "Backend", items: ["Django", "FastAPI", "REST APIs"] },
    { label: "AI & Data", items: ["Machine Learning", "Data Analytics", "Predictive Analysis"] },
  ];
  return (
    <section id="tech" className="py-20 lg:py-28 bg-muted/30 scroll-mt-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger} className="text-center mb-14">
          <motion.h2 variants={fadeUp} className="text-3xl font-bold sm:text-4xl">Technology <span className="gradient-text">Stack</span></motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-muted-foreground">Built with modern, production-grade technologies.</motion.p>
        </motion.div>
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} variants={stagger} className="grid gap-6 sm:grid-cols-3">
          {groups.map((g, i) => (
            <motion.div key={g.label} variants={fadeUp} custom={i} className="rounded-xl border border-border bg-card p-6 text-center">
              <h3 className="mb-4 text-sm font-semibold text-muted-foreground uppercase tracking-wider">{g.label}</h3>
              <div className="flex flex-wrap justify-center gap-2">
                {g.items.map((t) => (
                  <span key={t} className="rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm font-medium text-primary">{t}</span>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className="py-20 lg:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={stagger}
          className="relative overflow-hidden rounded-3xl gradient-bg px-8 py-16 text-center sm:px-16">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.08),transparent)]" />
          <div className="relative">
            <motion.h2 variants={fadeUp} className="text-3xl font-bold text-primary-foreground sm:text-4xl">Start Building a Greener Industry Today</motion.h2>
            <motion.p variants={fadeUp} custom={1} className="mx-auto mt-4 max-w-xl text-primary-foreground/80">Join the next generation of sustainable industrial management with AI-powered insights and real-time monitoring.</motion.p>
            <motion.div variants={fadeUp} custom={2} className="mt-8 flex flex-wrap justify-center gap-3">
              <Link to="/login"><Button size="lg" variant="secondary" className="px-6">Login</Button></Link>
              <Link to="/register"><Button size="lg" className="bg-primary-foreground/20 px-6 text-primary-foreground backdrop-blur-sm hover:bg-primary-foreground/30 border border-primary-foreground/20">Register</Button></Link>
              <Link to="/login"><Button size="lg" variant="outline" className="border-primary-foreground/30 px-6 text-primary-foreground hover:bg-primary-foreground/10">Explore Dashboard</Button></Link>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-border bg-muted/30 py-10">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-4 px-4 sm:flex-row sm:justify-between sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Leaf className="h-4 w-4 text-primary-foreground" />
          </div>
          <span className="font-semibold">SDMP</span>
        </div>
        <p className="text-xs text-muted-foreground">© {new Date().getFullYear()} Sustainability Data Monitoring Platform. All rights reserved.</p>
        <div className="flex gap-3">
          <a href="#" className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"><Github className="h-4 w-4" /></a>
          <a href="#" className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"><Linkedin className="h-4 w-4" /></a>
        </div>
      </div>
    </footer>
  );
}

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar />
      <HeroSection />
      <WhySection />
      <FeaturesSection />
      <HowItWorksSection />
      <AIAgentSection />
      <TechStackSection />
      <CTASection />
      <Footer />
    </div>
  );
}
