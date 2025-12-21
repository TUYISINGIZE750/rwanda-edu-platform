// Server Wake-Up Utility
const API_URL = import.meta.env.VITE_API_URL || 'https://rwanda-edu-platform.onrender.com/api/v1';

export async function wakeUpServer() {
  const maxAttempts = 20;
  const delayBetweenAttempts = 3000; // 3 seconds

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      // Try /api/v1/locations/provinces endpoint instead of /health
      const response = await fetch(`${API_URL}/locations/provinces`, {
        signal: controller.signal,
        headers: { 'Cache-Control': 'no-cache' }
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        return { success: true, attempts: attempt };
      }
    } catch (error) {
      if (attempt === maxAttempts) {
        return { success: false, error: 'Server failed to wake up' };
      }
      await new Promise(resolve => setTimeout(resolve, delayBetweenAttempts));
    }
  }

  return { success: false, error: 'Max attempts reached' };
}
