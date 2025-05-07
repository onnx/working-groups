# Why3Find Installation Guide

This guide sets up a full OCaml + Why3 + Alt-Ergo + `why3find` environment on **Ubuntu/Debian-based systems**.

---

## 🛠️ 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  curl \
  git \
  m4 \
  unzip \
  bubblewrap \
  pkg-config \
  libgmp-dev \
  libzmq3-dev \
  zlib1g-dev \
  libexpat1-dev \
  libgtk-3-dev \
  libgtksourceview-3.0-dev
```

---

## 🐫 2. Install OPAM & Initialize OCaml Environment

```bash
sudo apt-get install -y opam

opam init --disable-sandboxing -y
eval $(opam env)

opam switch create 4.13.0
eval $(opam env)
```

---

## 📦 3. Install OCaml Packages

```bash
opam install -y \
  "dune>=3.12" \
  "dune-site>=3.12" \
  "why3=1.8.0" \
  "yojson>=1.7.0" \
  "zmq>=5.0.0" \
  "terminal_size>=0.2.0"
```

---

## 🔍 4. Install `why3find`

### Option A: From OPAM

```bash
opam install why3find
```

### Option B: From Git Repository

```bash
git clone https://git.frama-c.com/pub/why3find.git
cd why3find
opam install .
```

---

## 🧪 5. Install Alt-Ergo with Tests

```bash
opam install -y alt-ergo=2.4.2 --with-test
```

---

## 📚 6. Install `odoc` with Documentation

```bash
opam install -y odoc --with-doc
```

---

## 🧹 7. Install VSCode Extension for Why3 Platform

```bash
wget https://git.frama-c.com/pub/why3find/-/jobs/1177337/artifacts/raw/vscode/why3-platform-1.1.1.vsix
code --install-extension why3-platform-1.1.1.vsix
```
