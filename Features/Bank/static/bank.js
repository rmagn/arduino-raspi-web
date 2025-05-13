// Coucou
// Fonctions globales pour l'import de fichiers
let handleFileImport;
let displayImportPreview;
let importOperations;
let currentSort = { column: null, asc: true };

document.addEventListener("DOMContentLoaded", () => {
  bindCategoryActions();
  bindOperationActions();

  // CREATE Category
  document.querySelector("#formCreateCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/categories", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const accordion = document.getElementById("categoriesAccordion");
      const temp = document.createElement("div");
      temp.innerHTML = createCategoryAccordionItem(result.category);
      accordion.appendChild(temp.firstElementChild);
      bindCategoryActions();
      form.reset();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalCreateCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // EDIT Category
  document.querySelector("#formEditCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/categories/edit", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const item = document.querySelector(`.accordion-item[data-id="${result.category.id}"]`);
      if (item) {
        const temp = document.createElement("div");
        temp.innerHTML = createCategoryAccordionItem(result.category);
        item.replaceWith(temp.firstElementChild);
        bindCategoryActions();
      }
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalEditCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // DELETE Category
  document.querySelector("#formDeleteCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector("[name='id']").value;
    const response = await fetch(`/bank/api/categories/${id}`, {
      method: "DELETE"
    });
    const result = await response.json();

    if (result.success) {
      document.querySelector(`.accordion-item[data-id="${id}"]`)?.remove();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalDeleteCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // CREATE SubCategory
  document.querySelector("#formCreateSubCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/subcategories", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const subcategoriesList = document.querySelector(`#subcategories-${result.subcategory.categorie_id}`);
      if (subcategoriesList) {
        const temp = document.createElement("div");
        temp.innerHTML = createSubCategoryItem(result.subcategory);
        subcategoriesList.appendChild(temp.firstElementChild);
        bindCategoryActions();
      }
      form.reset();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalCreateSubCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // EDIT SubCategory
  document.querySelector("#formEditSubCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/subcategories/edit", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const item = document.querySelector(`.subcategory-item[data-id="${result.subcategory.id}"]`);
      if (item) {
        const temp = document.createElement("div");
        temp.innerHTML = createSubCategoryItem(result.subcategory);
        item.replaceWith(temp.firstElementChild);
        bindCategoryActions();
      }
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalEditSubCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // DELETE SubCategory
  document.querySelector("#formDeleteSubCategory")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector("[name='id']").value;
    const response = await fetch(`/bank/api/subcategories/${id}`, {
      method: "DELETE"
    });
    const result = await response.json();

    if (result.success) {
      document.querySelector(`.subcategory-item[data-id="${id}"]`)?.remove();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalDeleteSubCategory")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // Operation event listeners
  document.querySelector("#formCreateOperation")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/operations", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const tbody = document.getElementById("operations-table-body");
      const temp = document.createElement("tbody");
      temp.innerHTML = createOperationRow(result.operation);
      tbody.appendChild(temp.firstElementChild);
      bindOperationActions();
      form.reset();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalCreateOperation")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  document.querySelector("#formEditOperation")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const response = await fetch("/bank/api/operations/edit", {
      method: "POST",
      body: data
    });
    const result = await response.json();

    if (result.success) {
      const row = document.querySelector(`tr[data-id="${result.operation.id}"]`);
      if (row) {
        row.outerHTML = createOperationRow(result.operation);
        bindOperationActions();
      }
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalEditOperation")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  document.querySelector("#formDeleteOperation")?.addEventListener("submit", async e => {
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector("[name='id']").value;
    const response = await fetch(`/bank/api/operations/${id}`, {
      method: "DELETE"
    });
    const result = await response.json();

    if (result.success) {
      document.querySelector(`tr[data-id="${id}"]`)?.remove();
      document.activeElement?.blur();
      bootstrap.Modal.getInstance(document.getElementById("modalDeleteOperation")).hide();
      showToast(result.message, "success");
    } else {
      showToast(result.message, "danger");
    }
  });

  // Gestion des sous-catégories dynamiques
  document.querySelectorAll("select[name='categorie_id']").forEach(select => {
    select.addEventListener("change", async e => {
      const categorieId = e.target.value;
      const sousCategorieSelect = e.target.closest(".row").querySelector("select[name='sous_categorie_id']");

      if (categorieId) {
        const response = await fetch(`/bank/api/categories/${categorieId}/subcategories`);
        const subcategories = await response.json();

        sousCategorieSelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
        subcategories.forEach(sub => {
          const option = document.createElement("option");
          option.value = sub.id;
          option.textContent = sub.nom;
          sousCategorieSelect.appendChild(option);
        });
      } else {
        sousCategorieSelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
      }
    });
  });

  // Fonction pour charger les sous-catégories d'une catégorie
  async function loadSubCategories(categoryId, targetSelect, selectedId = null) {
    if (!categoryId) {
      targetSelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
      return;
    }

    try {
      const response = await fetch(`/bank/api/categories/${categoryId}/subcategories`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const subcategories = await response.json();

      if (!Array.isArray(subcategories)) {
        throw new Error('La réponse de l\'API n\'est pas un tableau');
      }

      targetSelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
      subcategories.forEach(sub => {
        const option = document.createElement('option');
        option.value = sub.id;
        option.textContent = sub.nom;
        if (selectedId && sub.id === selectedId) {
          option.selected = true;
        }
        targetSelect.appendChild(option);
      });
    } catch (error) {
      console.error('Erreur lors du chargement des sous-catégories:', error);
      showToast('Erreur lors du chargement des sous-catégories', 'danger');
      targetSelect.innerHTML = '<option value="">-- Erreur de chargement --</option>';
    }
  }

  // Gestionnaire d'événements pour le changement de catégorie
  document.addEventListener('DOMContentLoaded', () => {
    // Pour le formulaire de création
    const createCategorySelect = document.querySelector('#modalCreateOperation select[name="categorie_id"]');
    const createSubCategorySelect = document.querySelector('#modalCreateOperation select[name="sous_categorie_id"]');

    if (createCategorySelect) {
      createCategorySelect.addEventListener('change', (e) => {
        loadSubCategories(e.target.value, createSubCategorySelect);
      });
    }

    // Pour le formulaire d'édition
    const editCategorySelect = document.querySelector('#modalEditOperation select[name="categorie_id"]');
    const editSubCategorySelect = document.querySelector('#modalEditOperation select[name="sous_categorie_id"]');

    if (editCategorySelect) {
      editCategorySelect.addEventListener('change', (e) => {
        loadSubCategories(e.target.value, editSubCategorySelect);
      });
    }

    // Gestionnaire pour le bouton d'édition d'opération
    document.querySelectorAll('.btn-edit-operation').forEach(button => {
      button.addEventListener('click', async () => {
        const modal = document.getElementById('modalEditOperation');
        const categoryId = button.dataset.categorie_id;
        const subCategoryId = button.dataset.sous_categorie_id;

        // Remplir les champs du formulaire
        modal.querySelector('[name="id"]').value = button.dataset.id;
        modal.querySelector('[name="date"]').value = button.dataset.date;
        modal.querySelector('[name="label"]').value = button.dataset.label;
        modal.querySelector('[name="amount"]').value = button.dataset.amount;
        modal.querySelector('[name="categorie_id"]').value = categoryId;
        modal.querySelector('[name="supplier"]').value = button.dataset.supplier;
        modal.querySelector('[name="person"]').value = button.dataset.person;

        // Charger les sous-catégories si une catégorie est sélectionnée
        if (categoryId) {
          await loadSubCategories(categoryId, modal.querySelector('[name="sous_categorie_id"]'), subCategoryId);
        }
      });
    });
  });

  // Initialisation des fonctions d'import
  handleFileImport = function (event) {
    console.log('Fichier sélectionné');
    const file = event.target.files[0];
    if (!file) {
      console.log('Aucun fichier sélectionné');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      try {
        console.log('Lecture du fichier');
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);
        console.log('Données brutes:', jsonData);

        // Fonction pour convertir une date Excel en date JavaScript
        const excelDateToJSDate = (excelDate) => {
          console.log('Conversion de la date:', excelDate);

          // Si c'est un nombre (format Excel)
          if (typeof excelDate === 'number') {
            // Les dates Excel sont comptées depuis le 1er janvier 1900
            // On soustrait 2 car Excel considère 1900 comme une année bissextile
            const date = new Date((excelDate - 25569) * 86400 * 1000);
            console.log('Date convertie:', date);
            return date.toISOString().split('T')[0];
          }

          // Si c'est une chaîne de caractères (format DD/MM/YYYY)
          if (typeof excelDate === 'string') {
            const [day, month, year] = excelDate.split('/');
            const date = new Date(year, month - 1, day);
            console.log('Date convertie:', date);
            return date.toISOString().split('T')[0];
          }

          console.error('Format de date non supporté:', excelDate);
          throw new Error('Format de date non supporté');
        };

        // Fonction pour nettoyer un libellé
        const cleanLabel = (label) => {
          return label
            .trim()
            .toUpperCase()
            .replace(/[^\w\s\d]/g, ' ')  // Supprimer les caractères spéciaux
            .replace(/\s+/g, '')         // Supprimer tous les espaces
            .substring(0, 50);           // Prendre les 50 premiers caractères
        };

        // Fonction pour trouver la clé de date
        const findDateKey = (row) => {
          return Object.keys(row).find(key => key.startsWith('Téléchargement du'));
        };

        // Traiter les données en ignorant les lignes d'en-tête (lignes 0 à 4)
        const operations = jsonData.slice(5).map(row => {
          // Trouver la clé de date
          const dateKey = findDateKey(row);
          console.log('Clé de date trouvée:', dateKey);
          console.log('Valeur de la date:', row[dateKey]);

          // Ignorer les lignes vides ou les lignes qui n'ont pas de date valide
          if (!row || typeof row !== 'object' || !dateKey ||
            typeof row[dateKey] !== 'number') {
            console.log('Ligne ignorée (vide ou invalide):', row);
            return null;
          }

          // Extraire les informations
          const date = excelDateToJSDate(row[dateKey]);
          const libelle = row['__EMPTY']?.trim() || '';
          const debit = parseFloat(row['__EMPTY_1']) || 0;
          const credit = parseFloat(row['__EMPTY_2']) || 0;
          const montant = debit ? -debit : credit;

          console.log('Opération traitée:', { date, libelle, debit, credit, montant });

          return {
            date: date,
            libelle: libelle,
            clean_libelle: cleanLabel(libelle),
            montant: montant,
            fournisseur: '',
            personne: ''
          };
        }).filter(op => op !== null); // Filtrer les lignes null

        console.log('Opérations traitées:', operations);
        displayImportPreview(operations);
      } catch (error) {
        console.error('Erreur lors de la lecture du fichier:', error);
        showToast('Erreur lors de la lecture du fichier', 'danger');
      }
    };
    reader.readAsArrayBuffer(file);
  };

  // Fonction pour supprimer une ligne de la prévisualisation
  window.removePreviewRow = function (button) {
    const tr = button.closest('tr');
    tr.remove();

    // Vérifier s'il reste des lignes
    const previewBody = document.getElementById('importPreviewBody');
    if (previewBody.children.length === 0) {
      const previewContainer = document.getElementById('importPreview');
      const importButton = document.getElementById('btnImportOperations');
      previewContainer.style.display = 'none';
      importButton.style.display = 'none';
    }
  };

  displayImportPreview = async function (operations) {
    console.log('Affichage de la prévisualisation');
    const previewContainer = document.getElementById('importPreview');
    const previewBody = document.getElementById('importPreviewBody');
    const importButton = document.getElementById('btnImportOperations');
    const spinnerImport = document.querySelector("#spinner-import");

    if (!previewContainer || !previewBody || !importButton) {
      console.error('Éléments de prévisualisation non trouvés');
      return;
    }

    spinnerImport.style.display = "block"; // Affiche le spinner
    try {
      // Récupérer les catégories
      const categoriesResponse = await fetch('/bank/api/categories');
      if (!categoriesResponse.ok) {
        throw new Error('Erreur lors de la récupération des catégories');
      }
      const categories = await categoriesResponse.json();

      // Vérifier les opérations existantes et obtenir les prédictions
      const response = await fetch('/bank/api/operations/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(operations)
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la vérification des opérations');
      }

      const result = await response.json();
      const existingOperations = result.existing_operations || [];
      const operationsWithPredictions = result.operations || operations;

      // Filtrer les opérations existantes
      const newOperations = operationsWithPredictions.filter(op => {
        return !existingOperations.some(existing =>
          existing.date === op.date &&
          existing.libelle === op.libelle &&
          existing.montant === op.montant
        );
      });

      // Vider le tableau
      previewBody.innerHTML = '';

      // Ajouter les opérations au tableau
      newOperations.forEach((op, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${op.date}</td>
          <td>${op.libelle}</td>
          <td>${op.montant < 0 ? (-op.montant).toFixed(2) : ''}</td>
          <td>${op.montant > 0 ? op.montant.toFixed(2) : ''}</td>
          <td>
            <select class="form-select form-select-sm category-select" data-index="${index}">
              <option value="">-- Sélectionner une catégorie --</option>
              ${categories.map(cat => `
                <option value="${cat.id}" ${op.categorie_id == cat.id ? 'selected' : ''}>
                  ${cat.nom}${op.categorie_id == cat.id ? ' (suggéré)' : ''}
                </option>
              `).join('')}
            </select>
          </td>
          <td>
            <select class="form-select form-select-sm subcategory-select" data-index="${index}" ${!op.categorie_id ? 'disabled' : ''}>
              <option value="">-- Sélectionner une sous-catégorie --</option>
            </select>
          </td>
          <td>
            <input type="text" class="form-control form-control-sm supplier-input" data-index="${index}" value="${op.fournisseur || ''}" placeholder="Fournisseur">
          </td>
          <td>
            <input type="text" class="form-control form-control-sm person-input" data-index="${index}" value="${op.personne || ''}" placeholder="Personne">
          </td>
          <td>
            <button type="button" class="btn btn-sm btn-danger" onclick="removePreviewRow(this)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
        `;
        previewBody.appendChild(tr);

        // Si une catégorie est prédite, charger les sous-catégories
        if (op.categorie_id) {
          loadSubCategories(op.categorie_id, tr.querySelector('.subcategory-select'), op.sous_categorie_id);
        }
      });

      // Ajouter les gestionnaires d'événements pour les catégories
      document.querySelectorAll('.category-select').forEach(select => {
        select.addEventListener('change', async (e) => {
          const index = e.target.dataset.index;
          const categoryId = e.target.value;
          const subcategorySelect = document.querySelector(`.subcategory-select[data-index="${index}"]`);

          if (categoryId) {
            try {
              const response = await fetch(`/bank/api/categories/${categoryId}/subcategories`);
              if (!response.ok) throw new Error('Erreur lors de la récupération des sous-catégories');

              const subcategories = await response.json();
              subcategorySelect.innerHTML = `
                <option value="">-- Sélectionner une sous-catégorie --</option>
                ${subcategories.map(sub => `<option value="${sub.id}">${sub.nom}</option>`).join('')}
              `;
              subcategorySelect.disabled = false;
            } catch (error) {
              console.error('Erreur:', error);
              showToast('Erreur lors du chargement des sous-catégories', 'danger');
            }
          } else {
            subcategorySelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
            subcategorySelect.disabled = true;
          }
        });
      });

      // Afficher le conteneur de prévisualisation et le bouton
      previewContainer.style.display = 'block';
      importButton.style.display = 'block';

      // Afficher un message détaillé sur les opérations existantes
      if (existingOperations.length > 0) {
        const message = existingOperations.map(op =>
          `- ${op.libelle} (${op.montant}€) du ${op.date} existe déjà (${op.existing_label} du ${op.existing_date})`
        ).join('\n');

        showToast(
          `${existingOperations.length} opération(s) déjà existante(s) ont été ignorée(s)\n${message}`,
          'warning'
        );
      }

      console.log('Prévisualisation affichée et bouton activé');
    } catch (error) {
      console.error('Erreur:', error);
      showToast('Erreur lors de la vérification des opérations', 'danger');
    } finally {
      spinnerImport.style.display = "none"; // Masque le spinner
    }
  };

  importOperations = async function () {
    const spinnerSubmit = document.querySelector("#spinner-submit");
    const previewBody = document.getElementById('importPreviewBody');
    if (!previewBody) {
      console.error('Tableau de prévisualisation non trouvé');
      return;
    }

    const operations = Array.from(previewBody.children).map(tr => {
      const cells = tr.children;
      const categorySelect = tr.querySelector('.category-select');
      const subcategorySelect = tr.querySelector('.subcategory-select');
      const supplierInput = tr.querySelector('.supplier-input');
      const personInput = tr.querySelector('.person-input');

      // Calcul du montant : si débit est présent, c'est un montant négatif, sinon c'est un crédit positif
      const debit = parseFloat(cells[2].textContent) || 0;
      const credit = parseFloat(cells[3].textContent) || 0;
      const montant = debit > 0 ? -debit : credit;

      // Récupérer les valeurs des sélecteurs
      const categorie_id = categorySelect?.value ? parseInt(categorySelect.value) : null;
      const sous_categorie_id = subcategorySelect?.value ? parseInt(subcategorySelect.value) : null;
      const fournisseur = supplierInput?.value || '';
      const personne = personInput?.value || '';

      console.log('Opération:', {
        date: cells[0].textContent,
        libelle: cells[1].textContent,
        montant: montant,
        categorie_id: categorie_id,
        sous_categorie_id: sous_categorie_id,
        fournisseur: fournisseur,
        personne: personne
      });

      return {
        date: cells[0].textContent,
        libelle: cells[1].textContent,
        montant: montant,
        categorie_id: categorie_id,
        sous_categorie_id: sous_categorie_id,
        fournisseur: fournisseur,
        personne: personne
      };
    });

    spinnerSubmit.style.display = "block"; // Affiche le spinner

    try {
      const response = await fetch('/bank/import', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(operations)
      });

      if (!response.ok) {
        throw new Error('Erreur lors de l\'import');
      }

      const result = await response.json();
      showToast(`${result.imported} opérations importées avec succès`, 'success');

      // Fermer le modal et recharger la liste
      const modal = bootstrap.Modal.getInstance(document.getElementById('modalImportOperations'));
      if (modal) {
        modal.hide();
      }
      location.reload();
    } catch (error) {
      console.error('Erreur:', error);
      showToast('Erreur lors de l\'import des opérations', 'danger');
    } finally {
      spinnerSubmit.style.display = "none"; // Masque le spinner
    }
  };

  // Gestion de l'import de fichiers
  const importFileInput = document.getElementById('importFile');
  const importButton = document.getElementById('btnImportOperations');

  if (importFileInput) {
    console.log('Input file trouvé');
    importFileInput.addEventListener('change', (event) => {
      console.log('Changement de fichier détecté');
      handleFileImport(event);
    });
  } else {
    console.error('Input file non trouvé');
  }

  if (importButton) {
    console.log('Bouton import trouvé');
    importButton.addEventListener('click', importOperations);
  } else {
    console.error('Bouton import non trouvé');
  }

  // Gestionnaire pour la fermeture du modal d'import
  const importModal = document.getElementById('modalImportOperations');
  if (importModal) {
    importModal.addEventListener('hidden.bs.modal', () => {
      // Réinitialiser le tableau de prévisualisation
      const previewBody = document.getElementById('importPreviewBody');
      if (previewBody) {
        previewBody.innerHTML = '';
      }

      // Masquer le conteneur de prévisualisation et le bouton d'import
      const previewContainer = document.getElementById('importPreview');
      const importButton = document.getElementById('btnImportOperations');
      if (previewContainer) {
        previewContainer.style.display = 'none';
      }
      if (importButton) {
        importButton.style.display = 'none';
      }

      // Réinitialiser le champ de fichier
      const fileInput = document.getElementById('importFile');
      if (fileInput) {
        fileInput.value = '';
      }
    });
  }


  // Gesstion graph analyse
  const categorySelect = document.getElementById("category-select");
  const barChartCanvas = document.getElementById("category-bar-chart").getContext("2d");
  const summaryTableBody = document.getElementById("summary-table-body");

  let barChart;

  // Fonction pour charger les données du graphique
  async function loadChartData(categoryId = null) {
    try {
      const response = await fetch(`/bank/api/analysis?category_id=${categoryId || ""}`);
      const data = await response.json();

      console.log("Données reçues :", data); // Ajoutez cette ligne pour inspecter les données


      // Mettre à jour le graphique
      const labels = data.last_six_months.map(item => item.month);
      const values = data.last_six_months.map(item => item.total);

      if (barChart) {
        barChart.destroy();
      }

      barChart = new Chart(barChartCanvas, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Montant total",
            data: values,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      });

      // Mettre à jour le tableau de synthèse
      summaryTableBody.innerHTML = data.last_four_months.map(item => `
        <tr>
          <td>${item.month}</td>
          <td class="text-danger">${parseFloat(item.debits || 0).toFixed(2)} €</td>
          <td class="text-success">${parseFloat(item.credits || 0).toFixed(2)} €</td>
          <td>${(parseFloat(item.credits || 0) + parseFloat(item.debits || 0)).toFixed(2)} €</td>
        </tr>
      `).join("");
    } catch (error) {
      console.error("Erreur lors du chargement des données :", error);
    }
  }

  // Charger les données initiales
  loadChartData();

  // Mettre à jour les données lorsque la catégorie change
  categorySelect.addEventListener("change", () => {
    const categoryId = categorySelect.value;
    loadChartData(categoryId);
  });

});

/**
 * Crée un élément d'accordéon pour une catégorie, comprenant son nom, le nombre de sous-catégories
 * et des boutons pour l'éditer et la supprimer, ainsi qu'un conteneur pour les sous-catégories.
 * @param {object} category - L'objet de la catégorie, comprenant les propriétés id et nom.
 * @returns {string} Le code HTML de l'élément d'accordéon.
 */
function createCategoryAccordionItem(category) {
  return `
  <div class="accordion-item" data-id="${category.id}">
    <h2 class="accordion-header" id="heading${category.id}">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${category.id}">
        ${category.nom}
        <span class="badge bg-primary rounded-pill ms-2">${category.sous_categories?.length || 0}</span>
      </button>
    </h2>
    <div id="collapse${category.id}" class="accordion-collapse collapse" data-bs-parent="#categoriesAccordion">
      <div class="accordion-body">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h6>Sous-catégories</h6>
          <div>
            <button class="btn btn-sm btn-link btn-edit-category" data-bs-toggle="modal" data-bs-target="#modalEditCategory"
              data-id="${category.id}" data-nom="${category.nom}">
              <i class="bi bi-pencil-square"></i>
            </button>
            <button class="btn btn-sm btn-link text-danger btn-delete-category" data-bs-toggle="modal" data-bs-target="#modalDeleteCategory"
              data-id="${category.id}" data-nom="${category.nom}">
              <i class="bi bi-trash"></i>
            </button>
            <button class="btn btn-sm btn-outline-primary" onclick="showAddSubCategoryModal(${category.id})">
              <i class="bi bi-plus"></i> Ajouter
            </button>
          </div>
        </div>
        <ul class="list-group" id="subcategories-${category.id}">
          ${category.sous_categories?.map(sub => createSubCategoryItem(sub)).join('') || ''}
        </ul>
      </div>
    </div>
  </div>`;
}

/**
 * Generates an HTML list item for a subcategory, including buttons for editing and deleting the subcategory.
 * @param {object} subcategory - The subcategory object containing the properties id and nom.
 * @returns {string} The HTML string for the subcategory list item.
 */

function createSubCategoryItem(subcategory) {
  return `
  <li class="list-group-item d-flex justify-content-between align-items-center subcategory-item" data-id="${subcategory.id}">
    ${subcategory.nom}
    <div>
      <button class="btn btn-sm btn-link" onclick="showEditSubCategoryModal(${subcategory.id}, '${subcategory.nom}')">
        <i class="bi bi-pencil-square"></i>
      </button>
      <button class="btn btn-sm btn-link text-danger" onclick="showDeleteSubCategoryModal(${subcategory.id}, '${subcategory.nom}')">
        <i class="bi bi-trash"></i>
      </button>
    </div>
  </li>`;
}

/**
 * Binds click event listeners to the edit and delete buttons of each category in the list.
 * The edit button will populate the edit category modal with the category's id and name.
 * The delete button will populate the delete category modal with the category's name and id.
 */
function bindCategoryActions() {
  document.querySelectorAll(".btn-edit-category").forEach(btn => {
    btn.addEventListener("click", () => {
      const modal = document.getElementById("modalEditCategory");
      modal.querySelector("[name='id']").value = btn.dataset.id;
      modal.querySelector("[name='nom']").value = btn.dataset.nom;
    });
  });

  document.querySelectorAll(".btn-delete-category").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("delete_category_nom").value = btn.dataset.nom;
      document.getElementById("delete_category_id").value = btn.dataset.id;
    });
  });
}

/**
 * Displays the modal for adding a new subcategory.
 * Sets the parent category ID in a hidden input field within the modal before displaying it.
 * 
 * @param {number} categoryId - The ID of the parent category to associate with the new subcategory.
 */

function showAddSubCategoryModal(categoryId) {
  document.getElementById("parentCategoryId").value = categoryId;
  const modal = new bootstrap.Modal(document.getElementById("modalCreateSubCategory"));
  modal.show();
}

/**
 * Displays the modal for editing a subcategory.
 * Sets the subcategory ID and name in the respective input fields within the modal before displaying it.
 * 
 * @param {number} subCategoryId - The ID of the subcategory to be edited.
 * @param {string} name - The name of the subcategory to be edited.
 */
function showEditSubCategoryModal(subCategoryId, name) {
  const modal = document.getElementById("modalEditSubCategory");
  modal.querySelector("[name='id']").value = subCategoryId;
  modal.querySelector("[name='nom']").value = name;
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

/**
 * Displays the modal for deleting a subcategory.
 * Sets the subcategory ID and name in the respective input fields within the modal before displaying it.
 * 
 * @param {number} subCategoryId - The ID of the subcategory to be deleted.
 * @param {string} name - The name of the subcategory to be deleted.
 */
function showDeleteSubCategoryModal(subCategoryId, name) {
  const modal = document.getElementById("modalDeleteSubCategory");
  modal.querySelector("#delete_subcategory_nom").value = name;
  modal.querySelector("#delete_subcategory_id").value = subCategoryId;
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

/**
 * Generates an HTML table row string for a given operation object.
 * The row includes operation details such as date, label, amount, category, subcategory, supplier, and person.
 * It also includes buttons for editing and deleting the operation.
 * The amount is displayed in red if it is a debit (negative) and in green if it is a credit (positive).
 * 
 * @param {Object} operation - The operation object containing details to populate the table row.
 * @param {number} operation.id - The unique identifier for the operation.
 * @param {string} operation.date - The date of the operation in a string format.
 * @param {string} operation.label - The label/description of the operation.
 * @param {number} operation.amount - The amount of the operation; indicates credit if positive, debit if negative.
 * @param {number} [operation.debit] - The debit amount if the operation is a debit.
 * @param {number} [operation.credit] - The credit amount if the operation is a credit.
 * @param {Object} [operation.categorie] - The category object, if available.
 * @param {string} [operation.categorie.nom] - The name of the category, if available.
 * @param {Object} [operation.sous_categorie] - The subcategory object, if available.
 * @param {string} [operation.sous_categorie.nom] - The name of the subcategory, if available.
 * @param {string} [operation.supplier] - The supplier related to the operation, if available.
 * @param {string} [operation.person] - The person related to the operation, if available.
 * @returns {string} - An HTML string representing a table row with operation details and action buttons.
 */

function createOperationRow(operation) {
  const amount = operation.amount;
  const isDebit = amount < 0;
  const displayAmount = isDebit ? operation.debit : operation.credit;

  return `
  <tr data-id="${operation.id}">
    <td>${new Date(operation.date).toLocaleDateString('fr-FR')}</td>
    <td>${operation.label}</td>
    <td class="${isDebit ? 'text-danger' : 'text-success'}">
      ${displayAmount.toFixed(2)} €
    </td>
    <td>${operation.categorie?.nom || ''}</td>
    <td>${operation.sous_categorie?.nom || ''}</td>
    <td>${operation.supplier || ''}</td>
    <td>${operation.person || ''}</td>
    <td>
      <button class="btn btn-sm btn-link btn-edit-operation" data-bs-toggle="modal" data-bs-target="#modalEditOperation"
        data-id="${operation.id}"
        data-date="${operation.date}"
        data-label="${operation.label}"
        data-amount="${operation.amount}"
        data-categorie_id="${operation.categorie_id || ''}"
        data-sous_categorie_id="${operation.sous_categorie_id || ''}"
        data-supplier="${operation.supplier || ''}"
        data-person="${operation.person || ''}">
        <i class="bi bi-pencil-square"></i>
      </button>
      <button class="btn btn-sm btn-link text-danger btn-delete-operation" data-bs-toggle="modal" data-bs-target="#modalDeleteOperation"
        data-id="${operation.id}"
        data-label="${operation.label}">
        <i class="bi bi-trash"></i>
      </button>
    </td>
  </tr>`;
}

/**
 * Binds click event listeners to the edit and delete buttons of each operation in the list.
 * The edit button will populate the edit operation modal with the operation's id, date, label, amount, category, subcategory, supplier, and person.
 * The delete button will populate the delete operation modal with the operation's name and id.
 */
function bindOperationActions() {
  document.querySelectorAll(".btn-edit-operation").forEach(btn => {
    btn.addEventListener("click", async () => {
      const modal = document.getElementById("modalEditOperation");
      modal.querySelector("[name='id']").value = btn.dataset.id;
      modal.querySelector("[name='date']").value = btn.dataset.date;
      modal.querySelector("[name='label']").value = btn.dataset.label;
      modal.querySelector("[name='amount']").value = btn.dataset.amount;

      const categorieSelect = modal.querySelector("[name='categorie_id']");
      const sousCategorieSelect = modal.querySelector("[name='sous_categorie_id']");

      // Sélectionner la catégorie
      categorieSelect.value = btn.dataset.categorie_id || '';

      // Charger et sélectionner la sous-catégorie
      if (btn.dataset.categorie_id) {
        try {
          const response = await fetch(`/bank/api/categories/${btn.dataset.categorie_id}/subcategories`);
          if (!response.ok) throw new Error('Erreur lors de la récupération des sous-catégories');

          const subcategories = await response.json();
          sousCategorieSelect.innerHTML = `
            <option value="">-- Sélectionner une sous-catégorie --</option>
            ${subcategories.map(sub => `<option value="${sub.id}">${sub.nom}</option>`).join('')}
          `;
          sousCategorieSelect.disabled = false;

          // Sélectionner la sous-catégorie
          if (btn.dataset.sous_categorie_id) {
            sousCategorieSelect.value = btn.dataset.sous_categorie_id;
          }
        } catch (error) {
          console.error('Erreur:', error);
          showToast('Erreur lors du chargement des sous-catégories', 'danger');
        }
      } else {
        sousCategorieSelect.innerHTML = '<option value="">-- Sélectionner une sous-catégorie --</option>';
        sousCategorieSelect.disabled = true;
      }

      modal.querySelector("[name='supplier']").value = btn.dataset.supplier;
      modal.querySelector("[name='person']").value = btn.dataset.person;
    });
  });

  document.querySelectorAll(".btn-delete-operation").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("delete_operation_label").value = btn.dataset.label;
      document.getElementById("delete_operation_id").value = btn.dataset.id;
    });
  });
}

/**
 * Displays a Bootstrap toast notification with a specified message and type.
 * The toast is appended to a container element identified by "toastContainer".
 * The toast will automatically disappear after a delay and be removed from the DOM.
 *
 * @param {string} message - The message to display inside the toast notification.
 * @param {string} [type="success"] - The type of toast to display, determining its background color.
 *                                    Accepts Bootstrap contextual class names such as 'success', 'danger', etc.
 */

function showToast(message, type = "success") {
  const toastContainer = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast align-items-center text-white bg-${type} border-0`;
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");

  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  `;

  toastContainer.appendChild(toast);
  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();

  toast.addEventListener("hidden.bs.toast", () => {
    toast.remove();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#operations-table-body");
  const filterInputs = document.querySelectorAll(".filter-input");
  const clearFiltersButton = document.querySelector("#clear-filters");
  let selectedDateRange = []; // Stocke la plage de dates sélectionnée

  // Fonction pour filtrer les lignes du tableau
  const filterTable = () => {
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    let total = 0;

    rows.forEach(row => {
      let isVisible = true;

      // Vérifiez chaque filtre de texte
      filterInputs.forEach(input => {
        const columnIndex = parseInt(input.dataset.column, 10);
        const filterValue = input.value.toLowerCase();
        const cellValue = row.children[columnIndex]?.textContent.toLowerCase() || "";

        // Si un filtre de texte ne correspond pas, la ligne est masquée
        if (filterValue && !cellValue.includes(filterValue)) {
          isVisible = false;
        }
      });

      // Vérifiez le filtre de plage de dates (colonne 0)
      if (selectedDateRange.length === 2) {
        const dateCell = row.children[0]?.textContent.trim(); // Colonne "Date"
        const rowDate = dateCell ? new Date(dateCell.split('/').reverse().join('-')) : null;
        const [startDate, endDate] = selectedDateRange;

        // Si la date de la ligne n'est pas dans la plage, la ligne est masquée
        if (!rowDate || rowDate < startDate || rowDate > endDate) {
          isVisible = false;
        }
      }

      // Appliquez la visibilité à la ligne
      row.style.display = isVisible ? "" : "none";

      // Si la ligne est visible, ajoutez son montant au total
      if (isVisible) {
        const amountCell = row.children[2]; // Colonne "Montant"
        const amount = parseFloat(amountCell?.textContent.replace(',', '.') || 0);
        total += amount;
      }
    });

    // NE PAS appeler sortTable() ici !
    // ... mise à jour du total ...
    const totalElement = document.getElementById("filtered-total");
    totalElement.textContent = `Total : ${total.toFixed(2).replace('.', ',')} €`;
  };

  // Ajoutez un écouteur d'événement pour chaque champ de filtre
  filterInputs.forEach(input => {
    input.addEventListener("input", filterTable);
  });

  // Initialisation du range date picker
  flatpickr("#date-range-picker", {
    mode: "range",
    dateFormat: "d/m/Y",
    onChange: (selectedDates) => {
      selectedDateRange = selectedDates; // Mettez à jour la plage de dates sélectionnée
      filterTable(); // Appliquez le filtre après la sélection de la plage
    },
  });

  // Gestion du bouton "Effacer les filtres"
  clearFiltersButton.addEventListener("click", () => {
    filterInputs.forEach(input => {
      input.value = ""; // Réinitialise les champs de filtre
    });
    selectedDateRange = []; // Réinitialise la plage de dates
    filterTable(); // Réaffiche toutes les lignes
  });

  // Ajoute un écouteur sur chaque en-tête sortable
  document.querySelectorAll('.sortable .sort-label').forEach(label => {
    label.addEventListener('click', function () {
      const header = this.closest('.sortable');
      const columnIndex = parseInt(header.dataset.column, 10);
      const asc = currentSort.column === columnIndex ? !currentSort.asc : true;
      currentSort = { column: columnIndex, asc };

      sortTable();
      updateSortIcons();
    });
  });

  // Fonction de tri
  function sortTable() {
    const rows = Array.from(tableBody.querySelectorAll('tr'));
    if (currentSort.column === null) return;

    rows.sort((a, b) => {
      const aText = a.children[currentSort.column]?.textContent.trim().toLowerCase() || '';
      const bText = b.children[currentSort.column]?.textContent.trim().toLowerCase() || '';
      if (!isNaN(aText) && !isNaN(bText)) {
        // Tri numérique si possible
        return currentSort.asc ? aText - bText : bText - aText;
      }
      return currentSort.asc ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });

    rows.forEach(row => tableBody.appendChild(row));
  }
});

function updateSortIcons() {
  document.querySelectorAll('.sortable').forEach(header => {
    const icon = header.querySelector('.sort-icon');
    const columnIndex = parseInt(header.dataset.column, 10);
    if (currentSort.column === columnIndex) {
      icon.textContent = currentSort.asc ? '▲' : '▼';
    } else {
      icon.textContent = '';
    }
  });
}