import { createRouter, createWebHistory } from "vue-router";
import Ontology from "../components/Ontology.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Ontology",
      component: Ontology,
    },
  ],
});

export default router;
