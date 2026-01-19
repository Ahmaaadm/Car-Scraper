import axios from 'axios';
import type { ScrapeResult } from './types';

const API_BASE = 'https://car-scraper-ev8b.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 minutes for scraping
});

export async function scrapeVehicle(url: string): Promise<ScrapeResult> {
  const response = await api.post('/scrape', { url });
  return response.data;
}

export async function downloadFolder(folderName: string): Promise<void> {
  const response = await api.get(`/download/${folderName}`, {
    responseType: 'blob'
  });

  // Create download link
  const blob = new Blob([response.data], { type: 'application/zip' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${folderName}.zip`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export async function deleteFolder(folderName: string): Promise<void> {
  await api.delete(`/delete/${folderName}`);
}
