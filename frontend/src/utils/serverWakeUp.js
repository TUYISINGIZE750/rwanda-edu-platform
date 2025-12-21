// Server Wake-Up Utility - Render free tier sleeps after 15min inactivity
// This wakes it up automatically when users visit
const API_URL = 'https://rwanda-edu-platform.onrender.com/api/v1';

export async function wakeUpServer() {
  const maxAttempts = 20;
  const delayBetweenAttempts = 3000;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      const response = await fetch(`${API_URL}/locations/provinces`, {
        signal: controller.signal,
        headers: { 'Cache-Control': 'no-cache' }
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        console.log(`✅ Server awake after ${attempt} attempts`);
        return { success: true, attempts: attempt };
      }
    } catch (error) {
      console.log(`⏳ Wake attempt ${attempt}/${maxAttempts}...`);
      if (attempt === maxAttempts) {
        return { success: false, error: 'Server failed to wake up' };
      }
      await new Promise(resolve => setTimeout(resolve, delayBetweenAttempts));
    }
  }

  return { success: false, error: 'Max attempts reached' };
}
