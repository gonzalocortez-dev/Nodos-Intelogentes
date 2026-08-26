const header = document.getElementById("header");
const nav = document.getElementById("nav");
const navToggle = document.getElementById("nav-toggle");
const form = document.getElementById("form-presupuesto");
const toast = document.getElementById("toast");
const lightbox = document.getElementById("lightbox");

const requiredFields = ["nombre", "telefono", "email", "ciudad", "tipo_propiedad", "servicio"];

function setHeaderState() {
  header.classList.toggle("is-scrolled", window.scrollY > 8);
}

window.addEventListener("scroll", setHeaderState, { passive: true });
setHeaderState();

navToggle.addEventListener("click", () => {
  const open = !nav.classList.contains("is-open");
  nav.classList.toggle("is-open", open);
  navToggle.setAttribute("aria-expanded", String(open));
});

nav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  });
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

document.querySelectorAll(".reveal").forEach((el, index) => {
  el.style.animationDelay = `${(index % 6) * 70}ms`;
  observer.observe(el);
});

function showToast(message, isError = false) {
  toast.hidden = false;
  toast.textContent = message;
  toast.style.background = isError ? "#3a151b" : "#2a2218";
  toast.style.borderColor = isError ? "#ff6b7a" : "#c4a06a";
  toast.style.color = isError ? "#ffd5da" : "#f3e6d0";
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    toast.hidden = true;
  }, 4200);
}

function setError(name, message) {
  const field = form.querySelector(`[name="${name}"]`);
  const wrap = field.closest(".field");
  const error = wrap.querySelector(".error");
  wrap.classList.toggle("has-error", Boolean(message));
  if (error) error.textContent = message || "";
}

function validEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function validPhone(value) {
  return value.replace(/\D/g, "").length >= 6;
}

function validateForm(data) {
  let ok = true;
  requiredFields.forEach((name) => setError(name, ""));

  if (data.nombre.trim().length < 3) {
    setError("nombre", "Ingresá tu nombre y apellido.");
    ok = false;
  }
  if (!validPhone(data.telefono)) {
    setError("telefono", "Ingresá un teléfono o WhatsApp válido.");
    ok = false;
  }
  if (!validEmail(data.email)) {
    setError("email", "Ingresá un email válido.");
    ok = false;
  }
  if (data.ciudad.trim().length < 2) {
    setError("ciudad", "Ingresá tu ciudad o localidad.");
    ok = false;
  }
  if (!data.tipo_propiedad) {
    setError("tipo_propiedad", "Seleccioná el tipo de propiedad.");
    ok = false;
  }
  if (!data.servicio) {
    setError("servicio", "Seleccioná un servicio.");
    ok = false;
  }
  return ok;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.origen = "landing";

  if (!validateForm(payload)) {
    showToast("Revisá los campos obligatorios.", true);
    return;
  }

  const button = document.getElementById("submit-btn");
  button.disabled = true;
  button.textContent = "Enviando...";

  try {
    const response = await fetch("/api/consultas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error("No pudimos enviar la consulta.");
    }
    form.reset();
    showToast(result.message || "Consulta enviada. Te vamos a contactar a la brevedad.");
  } catch (error) {
    showToast("No se pudo enviar. Probá de nuevo o escribinos por WhatsApp.", true);
  } finally {
    button.disabled = false;
    button.textContent = "Solicitar presupuesto";
  }
});

document.querySelectorAll(".gallery-item").forEach((item) => {
  item.addEventListener("click", () => {
    const img = lightbox.querySelector("img");
    img.src = item.dataset.src;
    img.alt = item.dataset.alt || "";
    lightbox.hidden = false;
  });
});

lightbox.querySelector(".lightbox-close").addEventListener("click", () => {
  lightbox.hidden = true;
});

lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.hidden = true;
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") lightbox.hidden = true;
});
