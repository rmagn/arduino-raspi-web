var scripts = {
    formatForDatetimeLocal: function(datetimeStr) {
        const d = new Date(datetimeStr);
        // Décalage compensé pour le champ local
        const offset = d.getTimezoneOffset(); // en minutes
        const localDate = new Date(d.getTime() - offset * 60000);
        return localDate.toISOString().slice(0, 16); // format "YYYY-MM-DDTHH:MM"
    }
}
    


