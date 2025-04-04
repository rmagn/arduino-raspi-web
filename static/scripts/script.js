var scripts = {
    formatForDatetimeLocal: function (datetimeStr) {
        const d = new Date(datetimeStr);
        // Décalage compensé pour le champ local
        const offset = d.getTimezoneOffset(); // en minutes
        const localDate = new Date(d.getTime() - offset * 60000);
        return localDate.toISOString().slice(0, 16); // format "YYYY-MM-DDTHH:MM"
    },

    formatDateFr: function (isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString("fr-FR", {
            weekday: "long", day: "numeric", month: "long", year: "numeric"
        });
    },

    formatTimeFr: function (isoString) {
        const date = new Date(isoString);
        return date.toLocaleTimeString("fr-FR", {
            hour: "2-digit", minute: "2-digit"
        });
    }

}



