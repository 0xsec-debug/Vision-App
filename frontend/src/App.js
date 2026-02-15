import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:5000/api';

const CameraIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
    <circle cx="12" cy="13" r="4"/>
  </svg>
);
const UploadIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="17 8 12 3 7 8"/>
    <line x1="12" y1="3" x2="12" y2="15"/>
  </svg>
);
const VideoIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <polygon points="23 7 16 12 23 17 23 7"/>
    <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
  </svg>
);
const SpinnerIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="spin">
    <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
  </svg>
);
const ScanIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/>
    <rect x="7" y="7" width="10" height="10" rx="1"/>
  </svg>
);
const XIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
);
const AlertIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="8" x2="12" y2="12"/>
    <line x1="12" y1="16" x2="12.01" y2="16"/>
  </svg>
);

const EMOTION_EMOJI = {
  happy:'😊', sad:'😢', angry:'😠', surprise:'😮',
  neutral:'😐', fear:'😨', disgust:'🤢'
};

export default function App() {
  const [mode, setMode]               = useState('camera');
  const [analysisType, setAnalysisType] = useState('all');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults]         = useState(null);
  const [error, setError]             = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl]   = useState(null);

  const webcamRef = useRef(null);
  const fileRef   = useRef(null);

  const clear = () => {
    setResults(null); setError(null);
    setSelectedFile(null); setPreviewUrl(null);
  };

  const handleFile = e => {
    const f = e.target.files[0];
    if (!f) return;
    setSelectedFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setResults(null); setError(null);
  };

  const analyze = async () => {
    try {
      setIsProcessing(true); setError(null); setResults(null);

      let endpoint = `${API_URL}/analyze-all`;
      if (analysisType === 'emotion') endpoint = `${API_URL}/detect-emotion`;
      else if (analysisType === 'fingers') endpoint = `${API_URL}/count-fingers`;
      else if (analysisType === 'objects') endpoint = `${API_URL}/count-objects`;

      let response;
      if (mode === 'camera') {
        const img = webcamRef.current?.getScreenshot();
        if (!img) throw new Error('Could not capture from camera');
        response = await axios.post(endpoint, { image: img, annotate: true });
      } else {
        if (!selectedFile) throw new Error('No file selected');
        const fd = new FormData();
        fd.append('file', selectedFile);
        response = await axios.post(`${endpoint}?annotate=true`, fd, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Analysis failed');
    } finally {
      setIsProcessing(false);
    }
  };

  const getEmotion = () => results?.emotion ?? (results?.faces_detected !== undefined ? results : null);
  const getFingers = () => results?.fingers ?? null;
  const getObjects = () => results?.objects ?? null;

  const showEmotion = analysisType === 'all' || analysisType === 'emotion';
  const showFingers = analysisType === 'all' || analysisType === 'fingers';
  const showObjects = analysisType === 'all' || analysisType === 'objects';

  return (
    <div className="App">

      {/* HEADER */}
      <header className="header">
        <div className="header-inner">
          <div className="header-logo">
            <div className="logo-icon">🤖</div>
            <div className="logo-text">
              <span className="logo-title">VisionAI</span>
              <span className="logo-sub">v1.0.0 · ISPARSH TIWARI</span>
            </div>
          </div>
          <div className="header-status">
            <div className="status-dot" />
            SYSTEM ONLINE
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="main-content">

        {/* Hero */}
        <div className="hero">
          <div className="hero-tag"><span>◈</span> AI VISION SYSTEM</div>
          <h1>Real-time <span>Computer Vision</span><br/>Analysis Platform</h1>
          <p>Detect facial expressions, count fingers and objects with state-of-the-art machine learning models.</p>
        </div>

        {/* Step 01 — Input Source */}
        <div>
          <div className="section-label">01 — Select Input Source</div>
          <div className="mode-selector">
            {[
              { id:'camera', icon:<CameraIcon/>, title:'Live Camera',   desc:'Real-time webcam feed' },
              { id:'image',  icon:<UploadIcon/>, title:'Upload Image',  desc:'JPG, PNG, GIF supported' },
              { id:'video',  icon:<VideoIcon/>,  title:'Upload Video',  desc:'MP4, AVI, MOV supported' },
            ].map(m => (
              <button key={m.id}
                className={`mode-btn ${mode === m.id ? 'active' : ''}`}
                onClick={() => { setMode(m.id); clear(); }}>
                <div className="mode-icon">{m.icon}</div>
                <div className="mode-info">
                  <div className="mode-title">{m.title}</div>
                  <div className="mode-desc">{m.desc}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Step 02 — Analysis Mode */}
        <div>
          <div className="section-label">02 — Analysis Configuration</div>
          <div className="analysis-selector">
            <label>ANALYSIS MODE</label>
            <div className="select-wrapper">
              <select value={analysisType} onChange={e => setAnalysisType(e.target.value)}>
                <option value="all">Full Analysis — Emotion + Fingers + Objects</option>
                <option value="emotion">Emotion Detection Only</option>
                <option value="fingers">Finger Counting Only</option>
                <option value="objects">Object Counting Only</option>
              </select>
            </div>
          </div>
        </div>

        {/* Step 03 — Input Feed */}
        <div>
          <div className="section-label">03 — Input Feed</div>
          <div className="input-area">
            {mode === 'camera' ? (
              <div className="camera-container">
                <Webcam ref={webcamRef} screenshotFormat="image/jpeg"
                  className="webcam"
                  videoConstraints={{ facingMode:'user', width:1280, height:720 }} />
                <div className="camera-overlay" />
              </div>
            ) : (
              <div className="upload-container">
                {previewUrl ? (
                  <div className="preview">
                    {mode === 'image'
                      ? <img src={previewUrl} alt="Preview" />
                      : <video src={previewUrl} controls />}
                  </div>
                ) : (
                  <div className="upload-placeholder" onClick={() => fileRef.current?.click()}>
                    <div className="upload-icon"><UploadIcon /></div>
                    <h3>Drop file here or click to browse</h3>
                    <p>{mode === 'image' ? 'JPG · PNG · GIF' : 'MP4 · AVI · MOV'}</p>
                  </div>
                )}
                <input ref={fileRef} type="file"
                  accept={mode === 'image' ? 'image/*' : 'video/*'}
                  onChange={handleFile} style={{ display:'none' }} />
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="action-buttons">
          <button className="analyze-btn" onClick={analyze}
            disabled={isProcessing || (mode !== 'camera' && !selectedFile)}>
            {isProcessing ? <><SpinnerIcon /> Processing...</> : <><ScanIcon /> Run Analysis</>}
          </button>
          {(results || error) && (
            <button className="clear-btn" onClick={clear}><XIcon /> Clear</button>
          )}
        </div>

        {/* Error */}
        {error && <div className="error-message"><AlertIcon /> {error}</div>}

        {/* Step 04 — Results */}
        {results && (
          <div className="results-container">
            <div className="section-label">04 — Analysis Results</div>

            {results.annotated_image && (
              <div className="annotated-image">
                <img src={results.annotated_image} alt="Annotated result" />
              </div>
            )}

            <div className="results-grid">

              {/* EMOTION */}
              {showEmotion && (() => {
                const ed = getEmotion();
                return (
                  <div className="result-card">
                    <div className="card-header">
                      <div className="card-icon emotion">😊</div>
                      <div>
                        <div className="card-title">Emotion Detection</div>
                        <div className="card-subtitle">FACIAL EXPRESSION ANALYSIS</div>
                      </div>
                    </div>
                    {ed && ed.faces_detected > 0 ? (
                      ed.emotions.map((e, i) => (
                        <div key={i} className="emotion-result">
                          <div className="emotion-primary">
                            <div className="emotion-name">{EMOTION_EMOJI[e.emotion]||'🎭'} {e.emotion}</div>
                            <div className="emotion-confidence">{e.confidence}%</div>
                          </div>
                          {e.all_probabilities && (
                            <div className="prob-bars">
                              {Object.entries(e.all_probabilities).sort((a,b)=>b[1]-a[1]).map(([label, prob]) => (
                                <div className="prob-row" key={label}>
                                  <span className="prob-label">{label}</span>
                                  <div className="prob-bar-track">
                                    <div className={`prob-bar-fill ${label===e.emotion?'top':''}`}
                                      style={{ width:`${prob}%` }} />
                                  </div>
                                  <span className="prob-value">{prob}%</span>
                                </div>
                              ))}
                            </div>
                          )}
                          {e.quote && <div className="emotion-quote">"{e.quote}"</div>}
                        </div>
                      ))
                    ) : (
                      <div className="no-detection"><AlertIcon /> No faces detected in frame</div>
                    )}
                  </div>
                );
              })()}

              {/* FINGERS */}
              {showFingers && (() => {
                const fd = getFingers();
                return (
                  <div className="result-card">
                    <div className="card-header">
                      <div className="card-icon fingers">🖐️</div>
                      <div>
                        <div className="card-title">Finger Counter</div>
                        <div className="card-subtitle">HAND LANDMARK DETECTION</div>
                      </div>
                    </div>
                    {fd && fd.hands_detected > 0 ? (
                      <>
                        <div className="finger-count-big">{fd.total_fingers}</div>
                        <div className="finger-count-label">FINGERS DETECTED</div>
                        <div className="finger-hands">
                          {fd.hands.map((h, i) => (
                            <div key={i} className="hand-row">
                              <span className="hand-label">{h.hand} hand</span>
                              <div className="hand-fingers">
                                {['Thumb','Index','Middle','Ring','Pinky'].map(name => (
                                  <div key={name}
                                    className={`finger-dot ${h.finger_status?.[name] ? 'up' : ''}`}
                                    title={name} />
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                        {fd.message && <div className="finger-message">{fd.message}</div>}
                      </>
                    ) : (
                      <div className="no-detection"><AlertIcon /> No hands detected in frame</div>
                    )}
                  </div>
                );
              })()}

              {/* OBJECTS */}
              {showObjects && (() => {
                const od = getObjects();
                return (
                  <div className="result-card">
                    <div className="card-header">
                      <div className="card-icon objects">🔍</div>
                      <div>
                        <div className="card-title">Object Counter</div>
                        <div className="card-subtitle">CONTOUR DETECTION</div>
                      </div>
                    </div>
                    {od ? (
                      <>
                        <div className="object-count-big">{od.count}</div>
                        <div className="object-count-label">OBJECTS DETECTED</div>
                        <div className="object-method">◈ Method: {od.method}</div>
                        {od.message && <div className="object-message">{od.message}</div>}
                      </>
                    ) : (
                      <div className="no-detection"><AlertIcon /> No objects detected</div>
                    )}
                  </div>
                );
              })()}

            </div>
          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-left">© 2026 VisionAI · Isparsh Tiwari</div>
          <div className="footer-right">
            <div className="footer-tag">Built with <span>React</span></div>
            <div className="footer-tag">Powered by <span>TensorFlow</span></div>
            <div className="footer-tag">CV via <span>MediaPipe</span></div>
          </div>
        </div>
      </footer>

    </div>
  );
}
