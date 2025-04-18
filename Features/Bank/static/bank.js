// Fonctions globales pour l'import de fichiers
let handleFileImport;
let displayImportPreview;
let importOperations;

document.addEventListener("DOMContentLoaded", () => {
  console.log('DOM chargé');
  
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
  handleFileImport = function(event) {
    console.log('Fichier sélectionné');
    const file = event.target.files[0];
    if (!file) {
      console.log('Aucun fichier sélectionné');
      return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        console.log('Lecture du fichier');
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);
        console.log('Données lues:', jsonData);
        
        // Fonction pour convertir une date Excel en date JavaScript
        const excelDateToJSDate = (excelDate) => {
          const date = new Date((excelDate - 25569) * 86400 * 1000);
          return date.toISOString().split('T')[0];
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
        
        // Traiter les données
        const operations = jsonData.map(row => {
          // Ignorer les lignes d'en-tête et les lignes vides
          if (!row['Téléchargement du 18/04/2025'] || typeof row['Téléchargement du 18/04/2025'] === 'string') {
            return null;
          }

          const date = excelDateToJSDate(row['Téléchargement du 18/04/2025']);
          const libelle = row['__EMPTY'] || '';
          const debit = row['__EMPTY_1'] || 0;
          const credit = row['__EMPTY_2'] || 0;
          const montant = debit ? -debit : credit;

          return {
            date: date,
            libelle: libelle,
            clean_libelle: cleanLabel(libelle),  // Ajouter le libellé nettoyé
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
  window.removePreviewRow = function(button) {
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

  displayImportPreview = async function(operations) {
    console.log('Affichage de la prévisualisation');
    const previewContainer = document.getElementById('importPreview');
    const previewBody = document.getElementById('importPreviewBody');
    const importButton = document.getElementById('btnImportOperations');

    if (!previewContainer || !previewBody || !importButton) {
      console.error('Éléments de prévisualisation non trouvés');
      return;
    }

    try {
      // Récupérer les catégories
      const categoriesResponse = await fetch('/bank/api/categories');
      if (!categoriesResponse.ok) {
        throw new Error('Erreur lors de la récupération des catégories');
      }
      const categories = await categoriesResponse.json();

      // Vérifier les opérations existantes
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

      // Filtrer les opérations existantes
      const newOperations = operations.filter(op => {
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
    }
  };

  importOperations = async function() {
    const previewBody = document.getElementById('importPreviewBody');
    if (!previewBody) {
      console.error('Tableau de prévisualisation non trouvé');
      return;
    }

    const operations = Array.from(previewBody.children).map(tr => {
      const cells = tr.children;
      const categorySelect = tr.querySelector('.category-select');
      const subcategorySelect = tr.querySelector('.subcategory-select');
      
      // Calcul du montant : si débit est présent, c'est un montant négatif, sinon c'est un crédit positif
      const debit = parseFloat(cells[2].textContent) || 0;
      const credit = parseFloat(cells[3].textContent) || 0;
      const montant = debit > 0 ? -debit : credit;
      
      return {
        date: cells[0].textContent,
        libelle: cells[1].textContent,
        montant: montant,
        categorie_id: categorySelect ? parseInt(categorySelect.value) : null,
        sous_categorie_id: subcategorySelect ? parseInt(subcategorySelect.value) : null,
        fournisseur: '',
        personne: ''
      };
    });

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
});

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

function showAddSubCategoryModal(categoryId) {
  document.getElementById("parentCategoryId").value = categoryId;
  const modal = new bootstrap.Modal(document.getElementById("modalCreateSubCategory"));
  modal.show();
}

function showEditSubCategoryModal(subCategoryId, name) {
  const modal = document.getElementById("modalEditSubCategory");
  modal.querySelector("[name='id']").value = subCategoryId;
  modal.querySelector("[name='nom']").value = name;
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

function showDeleteSubCategoryModal(subCategoryId, name) {
  const modal = document.getElementById("modalDeleteSubCategory");
  modal.querySelector("#delete_subcategory_nom").value = name;
  modal.querySelector("#delete_subcategory_id").value = subCategoryId;
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

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