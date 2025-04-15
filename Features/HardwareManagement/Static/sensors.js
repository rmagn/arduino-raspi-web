document.addEventListener("DOMContentLoaded", () => {
    bindSensorActions();
  
    // CREATE Sensor Alias
    document.querySelector("#formCreateSensor")?.addEventListener("submit", async e => {
      e.preventDefault();
      const form = e.target;
      const data = new FormData(form);
      const response = await fetch("/HardwareManagement/sensors/create", {
        method: "POST",
        body: data
      });
      const result = await response.json();
  
      if (result.success) {
        const tbody = document.querySelector("table tbody");
        const temp = document.createElement("tbody");
        temp.innerHTML = createSensorRow(result.alias);
        tbody.appendChild(temp.firstElementChild);
        bindSensorActions();
        form.reset();
        document.activeElement?.blur(); // juste avant hide()
        bootstrap.Modal.getInstance(document.getElementById("modalCreateSensor")).hide();
        scripts.showToast(result.message, "success");
      } else {
        scripts.showToast(result.message, "danger");
      }
    });
  
    // EDIT Sensor Alias
    document.querySelector("#formEditSensor")?.addEventListener("submit", async e => {
      e.preventDefault();
      const form = e.target;
      const data = new FormData(form);
      const response = await fetch("/HardwareManagement/sensors/edit", {
        method: "POST",
        body: data
      });
      const result = await response.json();
  
      if (result.success) {
        const row = document.querySelector(`tr[data-id="${result.alias.id}"]`);
        if (row) {
          const temp = document.createElement("tbody");
          temp.innerHTML = createSensorRow(result.alias);
          row.replaceWith(temp.firstElementChild);
          bindSensorActions();
        }
        document.activeElement?.blur(); // juste avant hide()
        bootstrap.Modal.getInstance(document.getElementById("modalEdit")).hide();
        scripts.showToast(result.message, "success");
      } else {
        scripts.showToast(result.message, "danger");
      }
    });
  
    // DELETE Sensor Alias
    document.querySelector("#formDeleteSensor")?.addEventListener("submit", async e => {
      e.preventDefault();
      const form = e.target;
      const id = form.querySelector("[name='id']").value;
      const response = await fetch("/HardwareManagement/sensors/delete", {
        method: "POST",
        body: new FormData(form)
      });
      const result = await response.json();
  
      if (result.success) {
        document.querySelector(`tr[data-id="${id}"]`)?.remove();
        document.activeElement?.blur(); // juste avant hide()
        bootstrap.Modal.getInstance(document.getElementById("modalDelete")).hide();
        scripts.showToast(result.message, "success");
      } else {
        scripts.showToast(result.message, "danger");
      }
    });
  });
  
  function createSensorRow(sensor) {
    return `
  <tr data-id="${sensor.id}">
    <td>${sensor.arduino_nom}</td>
    <td>Value${sensor.index_capteur}</td>
    <td>${sensor.alias}</td>
    <td>
      <button class="btn btn-sm btn-link btn-edit" data-bs-toggle="modal" data-bs-target="#modalEdit"
        data-id="${sensor.id}" data-arduino_id="${sensor.arduino_id}" data-index_capteur="${sensor.index_capteur}"
        data-sensor="${sensor.alias}">
        <i class="bi bi-pencil-square"></i>
      </button>
      <button class="btn btn-sm btn-link btn-delete" data-bs-toggle="modal" data-bs-target="#modalDelete"
        data-id="${sensor.id}" data-alias="${sensor.alias}">
        <i class="bi bi-trash"></i>
      </button>
    </td>
  </tr>`;
  }
  
  function bindSensorActions() {
    document.querySelectorAll(".btn-edit").forEach(btn => {
      btn.addEventListener("click", () => {
        const modal = document.getElementById("modalEdit");
        modal.querySelector("[name='id']").value = btn.dataset.id;
        modal.querySelector("[name='arduino_id']").value = btn.dataset.arduino_id;
        modal.querySelector("[name='index_capteur']").value = btn.dataset.index_capteur;
        modal.querySelector("[name='alias']").value = btn.dataset.alias;
      });
    });
  
    document.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", () => {
        document.getElementById("delete_alias_display").value = btn.dataset.alias;
        document.getElementById("delete_alias").value = btn.dataset.id;
      });
    });
  }
  