<template>
  <div class="home-container">
    <header class="header">
      <h1>歡迎來到首頁</h1>
      <p class="subtitle">探索我們的最新優惠和產品！</p>
    </header>
    <main>
      <section class="features">
        <h2>我們的特色 </h2>
        <div class="feature-item">
          <h3>🚀 快速送達</h3>
          <p>我們提供快速的外送服務，讓您無需等待！</p>
        </div>
        <div class="feature-item">
          <h3>🍽️ 多樣選擇</h3>
          <p>從美食到飲品，應有盡有，滿足您的味蕾！</p>
        </div>
        <div class="feature-item">
          <h3>💰 優惠活動</h3>
          <p>定期推出各種優惠活動，讓您享受更多折扣！</p>
        </div>
      </section>
      <div class="cta">
        <h2>立即訂購</h2>
        <button @click="goToOrderPage">開始選擇您的美食</button>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    goToOrderPage() {
      // 路由跳轉到外送頁面
      this.$router.push('/delivery');
    }
  }
};
</script>

<style scoped>
.home-container {
  text-align: center;
  padding: 20px;
  background:  linear-gradient(to right, #d8dbde, #46e27a); ;
}

.header {
  margin-bottom: 30px;
}

h1 {
  font-size: 2.5em;
  color: #170606;
  font-weight: bold;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2em;
  color: #7a7a7a;
  margin-bottom: 20px;
}

.features {
  display: flex;
  justify-content: space-around;
  margin-bottom: 50px;
}

.feature-item {
  max-width: 200px;
  background: hsl(288, 63%, 97%);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(223, 205, 205, 0.1);
}

h2 {
  font-size: 2em;
  color: #332826;
  margin-bottom: 20px;
}

h3 {
  font-size: 1.5em;
  color: #3a3a3a;
}

p {
  font-size: 1em;
  color: #555;
}

.cta {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
}

button:hover {
  background-color: #0056b3;
}
</style>
