export interface ScrapeResult {
  success: boolean;
  year?: string;
  title?: string;
  folder?: string;
  image_count?: number;
  total_images?: number;
  error?: string;
}
