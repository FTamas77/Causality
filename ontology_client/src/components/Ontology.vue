<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Build ontology for causal AI</h1>
        <hr><br><br>
        <alert_comp :message="message" v-if="showMessage"></alert_comp>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddParameterModal">
          Add Parameter
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Parameter</th>
              <th scope="col">Active</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(parameter, index) in selected_parameters" :key="index">
              <td>{{ parameter.name }}</td>
              <td>
                <span v-if="parameter.active">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" @click="toggleEditParameterModal(parameter)">
                    Update
                  </button>
                  <button type="button" class="btn btn-danger btn-sm" @click="handleDeleteParameter(parameter)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div>
        <v-network-graph class="graph" :nodes="nodes" :edges="edges" />
      </div>

    </div>

    <!-- add new parameter modal -->
    <div ref="addParameterModal" class="modal fade"
      :class="{ show: activeAddParameterModal, 'd-block': activeAddParameterModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new parameter</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleAddParameterModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addParameterName" class="form-label">Name:</label>
                <input type="text" class="form-control" id="addParameterName" v-model="addParameterForm.name"
                  placeholder="Enter name">
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="addParameterRead" v-model="addParameterForm.active">
                <label class="form-check-label" for="addParameterRead">Active</label>
              </div>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary btn-sm" @click="handleAddSubmit">
                  Submit
                </button>
                <button type="button" class="btn btn-danger btn-sm" @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddParameterModal" class="modal-backdrop fade show"></div>

    <!-- edit parameter modal -->
    <div ref="editParameterModal" class="modal fade"
      :class="{ show: activeEditParameterModal, 'd-block': activeEditParameterModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleEditParameterModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editParameterName" class="form-label">Name:</label>
                <input type="text" class="form-control" id="editParameterName" v-model="editParameterForm.name"
                  placeholder="Enter name">
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="editParameterRead" v-model="editParameterForm.active">
                <label class="form-check-label" for="editParameterRead">Active</label>
              </div>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary btn-sm" @click="handleEditSubmit">
                  Submit
                </button>
                <button type="button" class="btn btn-danger btn-sm" @click="handleEditCancel">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditParameterModal" class="modal-backdrop fade show"></div>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import { nodes, edges, size, hues } from "./data";

export default {
  data() {
    return {
      activeAddParameterModal: false,
      addParameterForm: {
        name: '',
        active: '',
      },
      // it has 
      //name: '',
      //active: ''
      selected_parameters: [],
      message: '',
      showMessage: false,
      activeEditParameterModal: false,
      editParameterForm: {
        name: '',
        active: ''
      },
      nodes,
      edges,
      size,
      hues,
    };
  },
  components: {
    alert_comp: Alert,
  },
  methods: {
    addParameter(payload) {
      const path = 'http://127.0.0.1:5000/ontology';
      axios.post(path, payload)
        .then(() => {
          this.getParameters();
          this.message = 'Parameter added!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getParameters();
        });
    },
    getParameters() {
      const path = 'http://127.0.0.1:5000/ontology';
      axios.get(path)
        .then((res) => {
          this.selected_parameters = res.data.parameters;

          // update the graph too
          for (const property in this.selected_parameters) {
            const node = {
              name: this.selected_parameters[property].name
            };

            nodes[this.selected_parameters[property].name] = node
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddParameterModal();
      let active = false;
      if (this.addParameterForm.active[0]) {
        active = true;
      }
      const payload = {
        name: this.addParameterForm.name,
        active,
      };
      this.addParameter(payload);
      this.initForm();
    },
    initForm() {
      this.addParameterForm.name = '';
      this.addParameterForm.active = [];
      this.editParameterForm.name = '';
      this.editParameterForm.active = [];
    },
    toggleAddParameterModal() {
      const body = document.querySelector('body');
      this.activeAddParameterModal = !this.activeAddParameterModal;
      if (this.activeAddParameterModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    toggleEditParameterModal(parameter) {
      if (parameter) {
        this.editParameterForm = parameter;
      }
      const body = document.querySelector('body');
      this.activeEditParameterModal = !this.activeEditParameterModal;
      if (this.activeEditParameterModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    handleEditSubmit() {
      this.toggleEditParameterModal(null);
      let active = false;
      if (this.editParameterForm.active) active = true;
      const payload = {
        name: this.editParameterForm.name,
        active,
      };
      this.updateParameter(payload, this.editParameterForm.name);
    },
    updateParameter(payload, par_name) {
      const path = `http://127.0.0.1:5000/ontology/${par_name}`;
      axios.put(path, payload)
        .then(() => {
          this.getParameters();
          this.message = 'Parameter updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getParameters();
        });
    },
    handleEditCancel() {
      this.toggleEditParameterModal(null);
      this.initForm();
      this.getParameters();
    },
    handleDeleteParameter(parameter) {
      this.removeParameter(parameter.name);
    },
    removeParameter(par_name) {
      const path = `http://127.0.0.1:5000/ontology/${par_name}`;
      axios.delete(path)
        .then(() => {
          this.getParameters();
          this.message = 'Parameter removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getParameters();
        });
    },
  },
  created() {
    this.getParameters();
  },
};
</script>

<style>
.graph {
  width: 800px;
  height: 600px;
  border: 1px solid #000;
}
</style>