const MOODS = [
  ['Chill','🌙','https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6'],
  ['Energetic','⚡','https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP'],
  ['Happy','😊','https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLusmQ'],
  ['Romantic','💕','https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn'],
  ['Food Mood','🍽️',null],
  ['Focus','🎯','https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ'],
  ['Party','🎉','https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif'],
  ['Cozy','☕','https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR'],
  ['Sad','😢','https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1']
];

const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = '/static/spotify.css';
document.head.appendChild(link);

const cells = MOODS.map(([label, emoji, url], i) =>
  `<button class="spotify-mood${i === 4 ? ' center' : ''}" data-url="${url || ''}">
     <span>${emoji}</span><span>${label}</span>
   </button>`).join('');

document.body.insertAdjacentHTML('beforeend', `
  <button class="spotify-btn" type="button">🎵</button>
  <div class="spotify-popup">
    <div class="spotify-head">
      <h3>🎵 Food Tunes</h3>
      <button class="spotify-x" type="button">&times;</button>
    </div>
    <div class="spotify-grid">${cells}</div>
    <div class="spotify-embed">
      <button class="spotify-back" type="button">&larr; Back</button>
      <iframe src="" allow="encrypted-media" loading="lazy"></iframe>
    </div>
  </div>
`);

const popup = document.querySelector('.spotify-popup');
const grid = document.querySelector('.spotify-grid');
const embed = document.querySelector('.spotify-embed');
const iframe = embed.querySelector('iframe');

document.querySelector('.spotify-btn').onclick = () => popup.classList.toggle('open');
document.querySelector('.spotify-x').onclick = () => popup.classList.remove('open');
document.querySelector('.spotify-back').onclick = () => {
  iframe.src = '';
  grid.style.display = 'grid';
  embed.classList.remove('show');
};

document.querySelectorAll('.spotify-mood').forEach(b => b.onclick = () => {
  let url = b.dataset.url;
  if (!url) {
    const others = MOODS.filter((_, i) => i !== 4);
    url = others[Math.floor(Math.random() * others.length)][2];
  }
  iframe.src = url.replace('open.spotify.com/', 'open.spotify.com/embed/');
  grid.style.display = 'none';
  embed.classList.add('show');
});
