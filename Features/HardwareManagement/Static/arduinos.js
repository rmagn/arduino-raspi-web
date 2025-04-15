document.addEventListener("DOMContentLoaded", () => {
  bindArduinoActions();

  document.querySelector("#formCreateArduino")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/HardwareManagement/arduinos/create", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const tbody = document.getElementById("arduino-table-body");
      tbody.insertAdjacentHTML("beforeend", createArduinoRow(result.arduino));

      // ✅ Déclare ici !
      const selects = document.querySelectorAll("select[name='arduino_id']");
      selects.forEach(select => {
        if (!Array.from(select.options).some(opt => opt.value == result.arduino.id)) {
          const option = document.createElement("option");
          option.value = result.arduino.id;
          option.textContent = result.arduino.nom;
          select.appendChild(option);
        }
      });

      bindArduinoActions();
      form.reset();
      document.activeElement?.blur(); // juste avant hide()
      bootstrap.Modal.getInstance(document.getElementById("modalCreateArduino")).hide();
      scripts.showToast(result.message, "success");
    }
    else {
      scripts.showToast(result.message, "danger");
    }
  });

  document.querySelector("#formEditArduino")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/HardwareManagement/arduinos/edit", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const row = document.querySelector(`tr[data-id="${result.arduino.id}"]`);
      if (row) {
        row.outerHTML = createArduinoRow(result.arduino);
        bindArduinoActions();
      }
      document.activeElement?.blur(); // juste avant hide()
      bootstrap.Modal.getInstance(document.getElementById("modalEditArduino")).hide();
      scripts.showToast(result.message, "success");
    } else {
      scripts.showToast(result.message, "danger");
    }
  });

  document.querySelector("#formDeleteArduino")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector("[name='id']").value;
    const response = await fetch("/HardwareManagement/arduinos/delete", {
      method: "POST",
      body: new FormData(form)
    });
    const result = await response.json();

    if (result.success) {
      document.querySelector(`tr[data-id="${id}"]`)?.remove();
      document.activeElement?.blur(); // juste avant hide()
      bootstrap.Modal.getInstance(document.getElementById("modalDeleteArduino")).hide();
      // ✅ Déclare ici !
      const selects = document.querySelectorAll("select[name='arduino_id']");
      selects.forEach(select => {
        const optionToRemove = select.querySelector(`option[value="${id}"]`);
        if (optionToRemove) {
          optionToRemove.remove();
        }
      });
      
      scripts.showToast(result.message, "success");
    } else {
      scripts.showToast(result.message, "danger");
    }
  });
});

function createArduinoRow(arduino) {
  return `
  <tr data-id="${arduino.id}">    
    <td>${arduino.id}</td>
    <td>${arduino.nom}</td>
    <td>${arduino.type}</td>
    <td>${arduino.adresse_ip || ''}</td>
    <td>
      <button class="btn btn-sm btn-link btn-edit-arduino" data-bs-toggle="modal" data-bs-target="#modalEditArduino"
        data-id="${arduino.id}" data-nom="${arduino.nom}" data-description="${arduino.description || ''}" data-type="${ arduino.type }" data-adresse_ip="${arduino.adresse_ip || ''}">
        <i class="bi bi-pencil-square"></i>
      </button>
      <button class="btn btn-sm btn-link btn-delete-arduino" data-bs-toggle="modal" data-bs-target="#modalDeleteArduino"
        data-id="${arduino.id}" data-nom="${arduino.nom}">
        <i class="bi bi-trash"></i>
      </button>
    </td>
  </tr>`;
}

function bindArduinoActions() {
  document.querySelectorAll(".btn-edit-arduino").forEach(btn => {
    btn.addEventListener("click", () => {
      const modal = document.getElementById("modalEditArduino");
      modal.querySelector("[name='id']").value = btn.dataset.id;
      modal.querySelector("[name='nom']").value = btn.dataset.nom;
      modal.querySelector("[name='description']").value = btn.dataset.description || "";
      modal.querySelector("[name='adresse_ip']").value = btn.dataset.adresse_ip || "";

      // Pour le select "type"
      const typeSelect = modal.querySelector("[name='type']");
      if (typeSelect) {
        typeSelect.value = btn.dataset.type;

      }
    });
  });

  document.querySelectorAll(".btn-delete-arduino").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("delete_arduino_nom").value = btn.dataset.nom;
      document.getElementById("delete_arduino_id").value = btn.dataset.id;
    });
  });
}
