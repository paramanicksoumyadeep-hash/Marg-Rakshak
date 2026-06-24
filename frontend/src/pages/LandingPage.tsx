
import { Link } from 'react-router-dom';
import { Shield, Map as MapIcon, Zap, Database, Camera, BrainCircuit, Target, FileText, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const LandingPage = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="min-h-[calc(100vh-80px)] bg-gray-50 dark:bg-[#09090b] transition-colors duration-500 flex flex-col items-center pt-24 pb-20 relative overflow-x-hidden selection:bg-red-500/30">
      
      {/* Premium Background Effects */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[20%] w-[600px] h-[600px] bg-red-600/10 dark:bg-red-500/5 rounded-full blur-[120px]" />
        <div className="absolute top-[20%] right-[10%] w-[500px] h-[500px] bg-yellow-500/10 dark:bg-orange-500/5 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] left-[40%] w-[800px] h-[800px] bg-blue-600/5 dark:bg-blue-500/5 rounded-full blur-[150px]" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.015] dark:opacity-[0.03] mix-blend-overlay"></div>
      </div>
      
      <motion.div 
        className="text-center max-w-6xl mx-auto px-6 relative z-10 w-full"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        
        {/* Top Badge */}
        <motion.div variants={itemVariants} className="flex justify-center mb-8">
          <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 text-gray-800 dark:text-gray-300 text-sm font-semibold backdrop-blur-md shadow-sm">
            <Shield className="text-red-600 dark:text-red-500" size={16} />
            <span className="tracking-wide uppercase text-xs">Bengaluru Traffic Police • Command Intelligence</span>
          </div>
        </motion.div>

        {/* Main Title */}
        <motion.div variants={itemVariants}>
          <h1 className="text-5xl sm:text-7xl md:text-[110px] font-black text-gray-900 dark:text-white leading-[1.1] md:leading-[1] tracking-tighter mb-4 drop-shadow-sm break-words">
            Marg Rakshak
          </h1>
        </motion.div>

        {/* Subtitle / Quote */}
        <motion.div variants={itemVariants}>
          <p className="text-2xl md:text-4xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-red-600 to-orange-500 dark:from-red-500 dark:to-orange-400 mb-8 tracking-tight">
            ಮಾರ್ಗ ರಕ್ಷಕ <span className="text-gray-400 dark:text-gray-600 font-light mx-2">|</span> <span className="italic">Guardian of Roads</span>
          </p>
        </motion.div>

        {/* Description */}
        <motion.p variants={itemVariants} className="text-lg md:text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-14 leading-relaxed font-medium">
          An advanced, highly-specialized AI ecosystem engineered for the streets of Bengaluru. 
          Detecting violations with <strong className="text-gray-900 dark:text-gray-200">surgical precision</strong> to ensure safer roads without compromising on accuracy.
        </motion.p>

        {/* Action Buttons */}
        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-4 sm:gap-5 mb-24 sm:mb-32 w-full max-w-2xl mx-auto">
          <Link 
            to="/generate-challan"
            className="group relative flex items-center justify-center gap-3 bg-gradient-to-b from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 dark:from-red-600 dark:to-red-800 text-white px-6 sm:px-8 py-4 rounded-2xl text-base sm:text-lg font-bold transition-all shadow-xl hover:shadow-2xl hover:shadow-red-600/20 hover:-translate-y-1 overflow-hidden w-full sm:w-auto"
          >
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out" />
            <Zap className="relative z-10 shrink-0" size={22} />
            <span className="relative z-10">Initiate Enforcement</span>
          </Link>

          <Link 
            to="/map"
            className="flex items-center gap-3 bg-white/80 dark:bg-gray-900/80 hover:bg-white dark:hover:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700 px-6 sm:px-8 py-4 rounded-2xl text-base sm:text-lg font-bold transition-all shadow-md hover:shadow-xl hover:-translate-y-1 backdrop-blur-md w-full sm:w-auto justify-center"
          >
            <MapIcon size={22} className="text-gray-500 dark:text-gray-400" />
            Live Surveillance Grid
          </Link>
        </motion.div>

        {/* Bento Grid - Project Overview */}
        <motion.div 
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-left w-full"
        >
          {/* Main Feature - Spans 2 columns */}
          <motion.div variants={itemVariants} className="lg:col-span-2 bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity group-hover:scale-110 duration-500">
              <BrainCircuit size={120} />
            </div>
            <div className="relative z-10">
              <div className="w-14 h-14 bg-red-100 dark:bg-red-900/30 rounded-2xl flex items-center justify-center mb-6 text-red-600 dark:text-red-400 shadow-sm border border-red-200 dark:border-red-800/50">
                <BrainCircuit size={28} />
              </div>
              <h3 className="text-3xl font-black text-gray-900 dark:text-white mb-4 tracking-tight">Zero-Trust AI Inference</h3>
              <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed max-w-xl">
                Powered by a custom-architected <strong>YOLOv8 framework</strong>, specifically fine-tuned for dense Indian traffic conditions. There is absolutely zero mock data; the engine performs real-time bounding-box regression on raw image arrays to identify vehicles, read plates, and classify offenses.
              </p>
            </div>
          </motion.div>

          <motion.div variants={itemVariants} className="bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl group hover:-translate-y-1 transition-transform duration-300">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center mb-5 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800/50">
              <Database size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">56,000+ Image Corpus</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Trained extensively on a highly diverse, manually annotated dataset of over 56,000 real-world images spanning every lighting condition, weather anomaly, and vehicle class on Bengaluru roads.
            </p>
          </motion.div>

          <motion.div variants={itemVariants} className="bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl group hover:-translate-y-1 transition-transform duration-300">
            <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/30 rounded-2xl flex items-center justify-center mb-5 text-emerald-600 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/50">
              <Camera size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Gov.in Integrated Feeds</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Surveillance topography and geospatial coordinates are seamlessly integrated directly from <strong>data.gov.in</strong>, ensuring 100% accurate spatial mapping of the 1,500+ active CCTV nodes.
            </p>
          </motion.div>

          <motion.div variants={itemVariants} className="bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl group hover:-translate-y-1 transition-transform duration-300">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center mb-5 text-purple-600 dark:text-purple-400 border border-purple-200 dark:border-purple-800/50">
              <Target size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Precision First</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Our uncompromising philosophy: <strong>Zero False Positives</strong>. It is infinitely better to issue a smaller volume of mathematically verifiable challans than to incorrectly penalize a single innocent citizen.
            </p>
          </motion.div>

          <motion.div variants={itemVariants} className="bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl group hover:-translate-y-1 transition-transform duration-300">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-2xl flex items-center justify-center mb-5 text-orange-600 dark:text-orange-400 border border-orange-200 dark:border-orange-800/50">
              <FileText size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Automated e-Challans</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Instantly bridges the gap between detection and enforcement. Detected anomalies are piped into an automated pipeline that drafts compliant e-challans complete with localized evidence.
            </p>
          </motion.div>

          {/* New Security Feature Card spanning full width of bottom row */}
          <motion.div variants={itemVariants} className="lg:col-span-3 bg-white/60 dark:bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-200/50 dark:border-gray-800/50 shadow-xl group hover:-translate-y-1 transition-transform duration-300">
            <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800/50 rounded-2xl flex items-center justify-center mb-5 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700/50">
              <ShieldCheck size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Enterprise-Grade Security</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed max-w-4xl">
              Project Drishti enforces strict security boundaries. The application features <strong>Secure httpOnly Session Cookies</strong> to defeat XSS, comprehensive <strong>OWASP Rate Limiting</strong> to prevent DDoS abuse, <strong>Strict MIME-type File Validation</strong> to sanitize uploads, and <strong>Cryptographic Password Hashing</strong>. We adhere strictly to zero-trust architecture.
            </p>
          </motion.div>

        </motion.div>
      </motion.div>
    </div>
  );
};

export default LandingPage;
