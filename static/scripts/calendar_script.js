var calendar_script = {
    colorMapCategories: {
        rdv_perso: "#b8b8b8",
        rdv_pro: "#d6d6d6",
        rdv_enfant: "#0d6efd",
        sport: "#d0c8b5",
        rdv: "#e3d8c4",
        anniversaire: "#ffc107",
        livraison: "#b7c8a3",
        conges: "#ffc107"
    },

    getColorCatergory: function (category) {
        return this.colorMapCategories[category] || "#0d6efd";
    },

    openEditEventModal: async function (event) {
        const form = document.getElementById("eventForm");
        form.reset(); // pour éviter les valeurs précédentes

        document.getElementById("modalEventTitle").innerText = "Modifier l’événement";

        // Chargement des calendriers AVANT de tenter la sélection
        await loadCalendarsSelect();

        form.querySelector("#event_id").value = event.id || "";
        form.querySelector("#subject").value = event.subject || "";
        form.querySelector("#location").value = event.location?.displayName || "";
        form.querySelector("#category").value = (event.categories && event.categories[0]) || "";


        const start = new Date(event.start?.dateTime);
        const end = new Date(event.end?.dateTime);
        form.querySelector("#start").value = scripts.formatForDatetimeLocal(event.start.dateTime);
        form.querySelector("#end").value = scripts.formatForDatetimeLocal(event.end.dateTime);

        const calendarId = event.calendarId || event.calendar_id;
        const select = form.querySelector("#calendar_id");
        const hiddenInput = form.querySelector("#calendar_id_hidden");

        if (calendarId) {
            const option = Array.from(select.options).find(opt => opt.value === calendarId);
            if (option) {
                select.value = calendarId;
            }
            // ✅ Copie la valeur vers le champ hidden pour garantir l'envoi
            if (hiddenInput) {
                hiddenInput.value = calendarId;
            }
        }

        select.setAttribute("disabled", true);

        const modal = new bootstrap.Modal(document.getElementById("modalEvent"));
        modal.show();
    },

    openCreateEventModal : function () {
        const form = document.getElementById("eventForm");
        form.reset();
        document.getElementById("modalEventTitle").innerText = "Créer un événement";
        form.querySelector("#event_id").value = "";

        // Activer le champ de calendrier
        form.querySelector("#calendar_id").removeAttribute("disabled");
        form.querySelector("#calendar_id_hidden").value = "";

        applyDurationPreset();

        // Charger les calendriers
        loadCalendarsSelect().then(() => {
            const modal = new bootstrap.Modal(document.getElementById("modalEvent"));
            modal.show();
        });
    }

};
