var fullcalendar_instance = null;

document.addEventListener('DOMContentLoaded', async function () {
  const calendarEl = document.getElementById('fullcalendar-container');
  if (!calendarEl) return;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'fr',
    buttonText: {
      today:    'Aujourd’hui',
      month:    'Mois',
      week:     'Semaine',
      day:      'Jour',
      list:     'Liste'
    },
    height: "auto",
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    slotMinTime: "06:00:00",
    slotMaxTime: "22:00:00",
    nowIndicator: true, // ligne rouge de l'heure actuelle (facultatif)
    events: async (fetchInfo, successCallback, failureCallback) => {
      try {
        const start = fetchInfo.startStr;
        const end = fetchInfo.endStr;

        const res = await fetch(`/api/calendar_events_range?start=${start}&end=${end}`);
        const rawEvents = await res.json();

        const formatted = rawEvents.map(ev => {
          const category = Array.isArray(ev.categories) ? ev.categories[0] : "";
          return {
            id: ev.id,
            title: ev.subject || "Sans titre",
            start: ev.start?.dateTime?.split(".")[0],
            end: ev.end?.dateTime?.split(".")[0],
            backgroundColor: calendar_script.getColorCatergory(category),
            extendedProps: {
              location: ev.location?.displayName || "",
              calendarId: ev.calendarId,
              category: category
            }
          };
        });

        successCallback(formatted);
      } catch (err) {
        console.error("❌ Erreur chargement événements FullCalendar :", err);
        failureCallback(err);
      }
    },
    eventClick: function (info) {
      const event = info.event;
      const ext = event.extendedProps;
    
      calendar_script.openEditEventModal({
        id: event.id,
        subject: event.title,
        start: { dateTime: event.start?.toISOString() },
        end: { dateTime: event.end?.toISOString() },
        location: { displayName: ext.location },
        calendarId: ext.calendarId,
        categories: [ext.category]
      });
    }
    
  });

  fullcalendar_instance = calendar;
  calendar.render();

  // 🔧 Corrige l'affichage si dans un onglet masqué au début
  const calendarTab = document.querySelector('#calendar-tab');
  if (calendarTab) {
    calendarTab.addEventListener('shown.bs.tab', function () {
      setTimeout(() => {
        fullcalendar_instance?.updateSize();
      }, 100);
    });
  }
});

// 🔄 Recalcul de taille sur redimensionnement de la fenêtre
window.addEventListener('resize', function () {
  fullcalendar_instance?.updateSize();
});
