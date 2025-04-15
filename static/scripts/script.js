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
    },

    showToast : function(message, type = 'success') {
        const toastContainer = document.getElementById("toastContainer");
        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.role = "alert";
        toast.innerHTML = `
          <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
          </div>`;
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        toast.addEventListener("hidden.bs.toast", () => toast.remove());
      }
      

}



