import { useState } from 'react';
import type { ScrapeResult } from './types';
import { scrapeVehicle, downloadFolder, deleteFolder } from './api';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [result, setResult] = useState<ScrapeResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [downloaded, setDownloaded] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim() || loading) return;

    setError(null);
    setResult(null);
    setDownloaded(false);
    setLoading(true);

    try {
      const data = await scrapeVehicle(url);
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to scrape vehicle');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to connect to server');
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload() {
    if (!result?.year || downloading) return;

    setDownloading(true);
    try {
      await downloadFolder(result.year);
      await deleteFolder(result.year);
      setDownloaded(true);
    } catch (err: any) {
      setError('Failed to download folder');
    } finally {
      setDownloading(false);
    }
  }

  function handleReset() {
    setUrl('');
    setResult(null);
    setError(null);
    setDownloaded(false);
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
            <h1>AutoSnap</h1>
          </div>
          <p>Download vehicle images from IAA Canada auctions</p>
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="error-banner">
            <svg className="error-icon" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
            </svg>
            {error}
          </div>
        )}

        <div className="card">
          {!result && !loading && (
            <>
              <form onSubmit={handleSubmit} className="url-form">
                <div className="input-group">
                  <label className="input-label">Vehicle Page URL</label>
                  <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://ca.iaai.com/vehicle-details/..."
                    className="url-input"
                    disabled={loading}
                  />
                </div>
                <button
                  type="submit"
                  className="submit-btn"
                  disabled={loading || !url.trim()}
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  Get Images
                </button>
              </form>

              <div className="instructions">
                <h2>How it works</h2>
                <ul className="steps">
                  <li className="step">
                    <span className="step-number">1</span>
                    <div className="step-content">
                      <p>Visit <a href="https://ca.iaai.com" target="_blank" rel="noreferrer">ca.iaai.com</a> and find a vehicle</p>
                    </div>
                  </li>
                  <li className="step">
                    <span className="step-number">2</span>
                    <div className="step-content">
                      <p>Open the vehicle details page</p>
                    </div>
                  </li>
                  <li className="step">
                    <span className="step-number">3</span>
                    <div className="step-content">
                      <p>Copy the URL and paste it above</p>
                    </div>
                  </li>
                  <li className="step">
                    <span className="step-number">4</span>
                    <div className="step-content">
                      <p>Click "Get Images" and download your ZIP</p>
                    </div>
                  </li>
                </ul>
              </div>
            </>
          )}

          {loading && (
            <div className="loading-section">
              <div className="spinner"></div>
              <p>Fetching vehicle images...</p>
            </div>
          )}

          {result && result.success && !downloaded && (
            <div className="success-section">
              <div className="success-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <h2>Images Ready!</h2>
              <div className="result-details">
                <div className="result-item">
                  <span className="label">Year</span>
                  <span className="value">{result.year}</span>
                </div>
                <div className="result-item">
                  <span className="label">Vehicle</span>
                  <span className="value">{result.title}</span>
                </div>
                <div className="result-item">
                  <span className="label">Images Found</span>
                  <span className="value">{result.image_count} photos</span>
                </div>
              </div>
              <button
                className="download-btn"
                onClick={handleDownload}
                disabled={downloading}
              >
                {downloading ? (
                  <>
                    <div className="spinner" style={{ width: 20, height: 20, margin: 0, borderWidth: 2 }}></div>
                    Preparing ZIP...
                  </>
                ) : (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                    Download {result.year}.zip
                  </>
                )}
              </button>
            </div>
          )}

          {downloaded && (
            <div className="success-section">
              <div className="success-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <h2>Download Complete!</h2>
              <p className="download-message">Your ZIP file has been saved to your downloads folder.</p>
              <button className="reset-btn" onClick={handleReset}>
                Download Another Vehicle
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        AutoSnap - Vehicle Image Downloader
      </footer>
    </div>
  );
}

export default App;
