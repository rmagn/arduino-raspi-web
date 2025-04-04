var meteo = {
    getWeatherIcon(symbol) {
        switch (symbol) {
          case 1: return '☀️'; // ciel clair
          case 2: return '🌤'; // peu nuageux
          case 3: return '⛅'; // partiellement nuageux
          case 4: return '☁️'; // très nuageux
          case 5: return '🌧'; // pluie faible
          case 6: return '🌧️'; // pluie modérée
          case 7: return '⛈'; // orage
          case 8: return '❄️'; // neige
          case 9: return '🌫️'; // brouillard
          case 101: return '🌙'; // ciel clair (nuit)
          case 102: return '🌤'; // peu nuageux (nuit)
          case 103: return '⛅'; // partiellement nuageux (nuit)
          case 104: return '☁️'; // très nuageux (nuit)
          default: return '❓';  // inconnu
        }
      }
}
  