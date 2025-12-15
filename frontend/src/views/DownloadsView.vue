<template>
  <div class="downloads-container">
    <div class="downloads-header">
      <h1>📚 Download Resources</h1>
      <p>Get guides and materials to help you get started</p>
    </div>

    <div class="downloads-grid">
      <!-- PDF Guide -->
      <div class="download-card">
        <div class="card-icon">📄</div>
        <h3>User Guide (PDF)</h3>
        <p>Complete guide for Students, Teachers, Admins & DOS with step-by-step instructions</p>
        <div class="card-details">
          <span class="file-size">10.5 KB</span>
          <span class="file-type">PDF</span>
        </div>
        <button @click="downloadPDF" class="download-btn pdf-btn">
          Download PDF
        </button>
      </div>

      <!-- PowerPoint Guide -->
      <div class="download-card">
        <div class="card-icon">🎨</div>
        <h3>Presentation (PowerPoint)</h3>
        <p>Professional 11-slide presentation covering all platform features and user roles</p>
        <div class="card-details">
          <span class="file-size">42 KB</span>
          <span class="file-type">PPTX</span>
        </div>
        <button @click="downloadPPT" class="download-btn ppt-btn">
          Download PowerPoint
        </button>
      </div>
    </div>

    <div class="downloads-info">
      <h2>What's Included?</h2>
      <div class="info-grid">
        <div class="info-item">
          <span class="info-icon">👨🎓</span>
          <h4>For Students</h4>
          <p>How to enroll, access materials, join live sessions</p>
        </div>
        <div class="info-item">
          <span class="info-icon">👨🏫</span>
          <h4>For Teachers</h4>
          <p>Create courses, upload materials, manage students</p>
        </div>
        <div class="info-item">
          <span class="info-icon">⚙️</span>
          <h4>For Admins</h4>
          <p>User management, course oversight, reports</p>
        </div>
        <div class="info-item">
          <span class="info-icon">📊</span>
          <h4>For DOS</h4>
          <p>Curriculum management, academic oversight</p>
        </div>
      </div>
    </div>

    <div class="back-button">
      <button @click="goBack" class="btn-back">← Back to Home</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DownloadsView',
  methods: {
    downloadPDF() {
      this.downloadFile('/guides/TSSANYWHERE_User_Guide.pdf', 'TSSANYWHERE_User_Guide.pdf');
    },
    downloadPPT() {
      this.downloadFile('/guides/TSSANYWHERE_User_Guide.pptx', 'TSSANYWHERE_User_Guide.pptx');
    },
    downloadFile(url, filename) {
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    goBack() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.downloads-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.downloads-header {
  text-align: center;
  color: white;
  margin-bottom: 50px;
}

.downloads-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.downloads-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.downloads-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 900px;
  margin: 0 auto 50px;
}

.download-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
}

.download-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.download-card h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 10px;
}

.download-card p {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 20px;
  line-height: 1.5;
}

.card-details {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
  font-size: 0.85rem;
}

.file-size, .file-type {
  background: #f0f0f0;
  padding: 5px 12px;
  border-radius: 20px;
  color: #555;
}

.download-btn {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pdf-btn {
  background: #FF6B6B;
  color: white;
}

.pdf-btn:hover {
  background: #ee5a52;
  transform: scale(1.02);
}

.ppt-btn {
  background: #4ECDC4;
  color: white;
}

.ppt-btn:hover {
  background: #45b8af;
  transform: scale(1.02);
}

.downloads-info {
  background: white;
  border-radius: 12px;
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.downloads-info h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.info-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 10px;
}

.info-item h4 {
  color: #333;
  margin-bottom: 8px;
}

.info-item p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.back-button {
  text-align: center;
}

.btn-back {
  background: white;
  color: #667eea;
  border: 2px solid white;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: transparent;
  color: white;
}

@media (max-width: 768px) {
  .downloads-header h1 {
    font-size: 1.8rem;
  }

  .downloads-grid {
    grid-template-columns: 1fr;
  }

  .downloads-info {
    padding: 20px;
  }
}
</style>
