import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
import time
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import zscore
import warnings
warnings.filterwarnings("ignore")

def hex_to_rgba(hex_color, alpha=0.12):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

st.set_page_config(
    page_title="SmartCharge AI ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

:root{
  --c1:#00f5d4; --c2:#7b2fff; --c3:#ff006e; --c4:#fb5607; --c5:#ffbe0b;
  --glass-bg:rgba(255,255,255,0.04);
  --glass-border:rgba(255,255,255,0.12);
  --glass-shadow:0 8px 32px rgba(0,0,0,0.55);
  --glow-cyan:0 0 25px rgba(0,245,212,0.65);
  --glow-purple:0 0 25px rgba(123,47,255,0.65);
  --glow-pink:0 0 25px rgba(255,0,110,0.65);
}

/* === BACKGROUND === */
.stApp {
  background: #000510;
  font-family: 'Rajdhani', sans-serif;
  color: rgba(255,255,255,0.92);
  overflow-x: hidden;
}
.stApp::before {
  content: '';
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background:
    radial-gradient(ellipse 80% 60% at 15% 20%, rgba(0,245,212,0.11) 0%, transparent 60%),
    radial-gradient(ellipse 60% 70% at 85% 15%, rgba(123,47,255,0.09) 0%, transparent 60%),
    radial-gradient(ellipse 70% 50% at 50% 85%, rgba(255,0,110,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 40% 40% at 70% 50%, rgba(251,86,7,0.05) 0%, transparent 50%);
  animation: blobPulse 14s ease-in-out infinite alternate;
  pointer-events: none; z-index: 0;
}
@keyframes blobPulse {
  0%   { transform: scale(1)    translate(0px,0px); }
  33%  { transform: scale(1.05) translate(-18px,12px); }
  66%  { transform: scale(0.97) translate(14px,-8px); }
  100% { transform: scale(1.03) translate(-8px,18px); }
}
.stApp::after {
  content: '';
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-image:
    linear-gradient(rgba(0,245,212,0.022) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,212,0.022) 1px, transparent 1px);
  background-size: 55px 55px;
  animation: gridDrift 28s linear infinite;
  pointer-events: none; z-index: 0;
}
@keyframes gridDrift {
  0%   { transform: translateY(0)  translateX(0); }
  100% { transform: translateY(55px) translateX(0); }
}

/* === PAGE TRANSITION === */
@keyframes pageSlideIn {
  0%   { opacity:0; transform: translateY(44px) scale(0.96); filter: blur(10px); }
  100% { opacity:1; transform: translateY(0)    scale(1);    filter: blur(0);    }
}
@keyframes staggerUp {
  0%   { opacity:0; transform: translateY(20px); }
  100% { opacity:1; transform: translateY(0);    }
}

/* === CLAYMORPHISM CARD === */
.clay-card {
  background: linear-gradient(145deg,
    rgba(0,245,212,0.09) 0%,
    rgba(123,47,255,0.06) 50%,
    rgba(255,0,110,0.04) 100%);
  border-radius: 28px;
  border: 1.5px solid rgba(255,255,255,0.16);
  padding: 28px;
  box-shadow:
    0 22px 60px rgba(0,0,0,0.55),
    0 4px 0 rgba(255,255,255,0.055) inset,
    0 -2px 0 rgba(0,0,0,0.3) inset,
    8px 8px 30px rgba(0,0,0,0.4),
    -4px -4px 14px rgba(255,255,255,0.038);
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  position: relative; overflow: hidden;
  transition: all 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.clay-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 45%;
  background: linear-gradient(180deg, rgba(255,255,255,0.065) 0%, transparent 100%);
  border-radius: 28px 28px 0 0; pointer-events: none;
}
.clay-card::after {
  content: '';
  position: absolute; top: 0; left: -130%; width: 70%; height: 100%;
  background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,0.055) 50%, transparent 70%);
  transition: left 0.75s ease; pointer-events: none;
}
.clay-card:hover::after { left: 160%; }
.clay-card:hover {
  transform: translateY(-10px) scale(1.015);
  border-color: rgba(0,245,212,0.42);
  box-shadow:
    0 30px 80px rgba(0,0,0,0.65),
    0 0 40px rgba(0,245,212,0.18),
    0 4px 0 rgba(255,255,255,0.07) inset,
    0 -2px 0 rgba(0,0,0,0.3) inset;
}

/* === SKEUOMORPHIC CARD === */
.skeuo-card {
  background: linear-gradient(160deg,
    rgba(255,255,255,0.085) 0%,
    rgba(255,255,255,0.028) 40%,
    rgba(0,0,0,0.18) 100%);
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.11);
  padding: 24px;
  box-shadow:
    7px 7px 18px rgba(0,0,0,0.58),
    -4px -4px 10px rgba(255,255,255,0.045),
    inset 1px 1px 2px rgba(255,255,255,0.11),
    inset -1px -1px 2px rgba(0,0,0,0.38);
  backdrop-filter: blur(14px);
  transition: all 0.3s ease;
  position: relative;
}
.skeuo-card:hover {
  box-shadow:
    3px 3px 8px rgba(0,0,0,0.68),
    -2px -2px 5px rgba(255,255,255,0.05),
    inset 1px 1px 2px rgba(255,255,255,0.09),
    inset -1px -1px 2px rgba(0,0,0,0.45),
    0 0 20px rgba(0,245,212,0.13);
  transform: translateY(-3px);
}

/* === LIQUID GLASS CARD === */
.liquid-glass {
  background: linear-gradient(135deg,
    rgba(255,255,255,0.075) 0%,
    rgba(255,255,255,0.025) 50%,
    rgba(0,245,212,0.038) 100%);
  backdrop-filter: blur(38px) saturate(175%) brightness(1.08);
  -webkit-backdrop-filter: blur(38px) saturate(175%) brightness(1.08);
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.18);
  border-top: 1px solid rgba(255,255,255,0.32);
  border-left: 1px solid rgba(255,255,255,0.22);
  box-shadow:
    0 14px 50px rgba(0,0,0,0.5),
    0 1px 0 rgba(255,255,255,0.18) inset,
    0 -1px 0 rgba(0,0,0,0.18) inset;
  padding: 28px;
  position: relative; overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.liquid-glass::before {
  content: '';
  position: absolute; top: -35%; right: -25%;
  width: 65%; height: 65%;
  background: radial-gradient(circle, rgba(0,245,212,0.07) 0%, transparent 70%);
  animation: liquidBlob 7s ease-in-out infinite alternate;
  pointer-events: none;
}
@keyframes liquidBlob {
  0%   { transform: scale(1)   translate(0,0)       rotate(0deg); }
  100% { transform: scale(1.35) translate(-22px,16px) rotate(32deg); }
}
.liquid-glass:hover {
  border-color: rgba(0,245,212,0.32);
  box-shadow:
    0 22px 65px rgba(0,0,0,0.6),
    0 0 32px rgba(0,245,212,0.14),
    0 1px 0 rgba(255,255,255,0.22) inset;
  transform: translateY(-6px);
}

/* === METRIC CARDS === */
.metric-box {
  background: linear-gradient(145deg,
    rgba(0,245,212,0.075) 0%,
    rgba(123,47,255,0.055) 60%,
    rgba(0,0,0,0.18) 100%);
  border: 1.5px solid rgba(0,245,212,0.2);
  border-radius: 20px; padding: 22px; text-align: center;
  box-shadow:
    6px 6px 18px rgba(0,0,0,0.5),
    -3px -3px 8px rgba(255,255,255,0.038),
    inset 0 1px 1px rgba(255,255,255,0.09);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative; overflow: hidden; cursor: default;
}
.metric-box::after {
  content: '';
  position: absolute; top: -60%; left: -60%;
  width: 220%; height: 220%;
  background: conic-gradient(transparent 0deg, rgba(0,245,212,0.10) 90deg, transparent 180deg);
  animation: conicSpin 4.5s linear infinite;
  opacity: 0; transition: opacity 0.3s;
}
.metric-box:hover::after { opacity: 1; }
@keyframes conicSpin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
.metric-box:hover {
  transform: translateY(-8px) scale(1.04);
  border-color: var(--c1);
  box-shadow:
    0 20px 50px rgba(0,0,0,0.6), var(--glow-cyan),
    3px 3px 10px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.11);
}
.metric-val {
  font-family: 'Orbitron', monospace; font-size: 2.05rem; font-weight: 900;
  background: linear-gradient(90deg, var(--c1), var(--c2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  position: relative; z-index: 1;
}
.metric-label {
  font-family: 'Share Tech Mono', monospace; font-size: 0.76rem;
  color: rgba(255,255,255,0.48); letter-spacing: 2.5px; text-transform: uppercase;
  margin-top: 5px; position: relative; z-index: 1;
}

/* === HEADINGS === */
h1, h2, h3 {
  font-family: 'Orbitron', monospace !important;
  background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3), var(--c1));
  background-size: 300% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: gradientSlide 7s linear infinite;
}
@keyframes gradientSlide {
  0%   { background-position: 0%   50%; }
  100% { background-position: 300% 50%; }
}

.section-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase;
  color: var(--c1); margin-bottom: 18px;
  display: flex; align-items: center; gap: 10px;
}
.section-title::before {
  content: '';
  display: inline-block; width: 4px; height: 22px;
  background: linear-gradient(var(--c1), var(--c2));
  border-radius: 3px; box-shadow: 0 0 8px rgba(0,245,212,0.7);
}

/* === SPLASH === */
.splash-wrap {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; min-height: 80vh; gap: 28px; text-align: center;
  animation: pageSlideIn 0.8s ease both;
}
.splash-logo {
  font-family: 'Orbitron', monospace; font-size: 4.2rem; font-weight: 900;
  background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3), var(--c4), var(--c1));
  background-size: 400% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: gradientSlide 2.5s linear infinite;
  filter: drop-shadow(0 0 28px rgba(0,245,212,0.38));
}
.splash-sub {
  font-family: 'Share Tech Mono', monospace; color: var(--c1);
  font-size: 0.9rem; letter-spacing: 5px;
  animation: typeBlink 1.3s step-end infinite;
}
@keyframes typeBlink { 0%,100%{opacity:1} 50%{opacity:0} }
.pulse-ring {
  width: 155px; height: 155px; border-radius: 50%;
  border: 2px solid rgba(0,245,212,0.38);
  display: flex; align-items: center; justify-content: center; font-size: 3.2rem;
  background: linear-gradient(145deg, rgba(0,245,212,0.055), rgba(123,47,255,0.038));
  box-shadow:
    0 0 0 0 rgba(0,245,212,0.3),
    6px 6px 20px rgba(0,0,0,0.5),
    -4px -4px 12px rgba(255,255,255,0.038),
    inset 0 2px 4px rgba(255,255,255,0.08);
  animation: pulseExpand 2.2s ease-out infinite;
}
@keyframes pulseExpand {
  0%   { box-shadow: 0 0 0 0 rgba(0,245,212,0.5), 6px 6px 20px rgba(0,0,0,0.5), -4px -4px 12px rgba(255,255,255,0.038); }
  70%  { box-shadow: 0 0 0 50px rgba(0,245,212,0), 6px 6px 20px rgba(0,0,0,0.5), -4px -4px 12px rgba(255,255,255,0.038); }
  100% { box-shadow: 0 0 0 0 rgba(0,245,212,0),   6px 6px 20px rgba(0,0,0,0.5), -4px -4px 12px rgba(255,255,255,0.038); }
}

/* === HERO LANDING === */
.hero-wrapper {
  text-align: center; padding: 68px 20px 38px;
  animation: pageSlideIn 0.75s ease both;
}
.hero-badge {
  display: inline-block; padding: 7px 22px; border-radius: 30px;
  border: 1.5px solid rgba(0,245,212,0.42);
  background: rgba(0,245,212,0.065);
  font-size: 0.77rem; color: var(--c1); letter-spacing: 3px;
  font-family: 'Share Tech Mono', monospace; margin-bottom: 26px;
  box-shadow: 0 4px 14px rgba(0,245,212,0.14), inset 0 1px 0 rgba(255,255,255,0.10);
  animation: staggerUp 0.5s 0.2s ease both;
}
.hero-title {
  font-family: 'Orbitron', monospace; font-size: 3.8rem; font-weight: 900;
  background: linear-gradient(135deg, var(--c1) 0%, var(--c2) 50%, var(--c3) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  line-height: 1.15; margin-bottom: 14px;
  filter: drop-shadow(0 0 38px rgba(0,245,212,0.18));
  animation: staggerUp 0.7s 0.1s ease both;
}
.hero-sub {
  font-family: 'Rajdhani', sans-serif; font-size: 1.12rem;
  color: rgba(255,255,255,0.42); letter-spacing: 5px; text-transform: uppercase;
  margin-bottom: 34px; animation: staggerUp 0.7s 0.3s ease both;
}
.feature-strip {
  display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; margin: 26px 0;
  animation: staggerUp 0.7s 0.5s ease both;
}
.feature-pill {
  padding: 10px 20px; border-radius: 30px;
  background: linear-gradient(145deg, rgba(255,255,255,0.055), rgba(0,0,0,0.18));
  border: 1px solid rgba(255,255,255,0.11);
  font-size: 0.83rem; color: rgba(255,255,255,0.62);
  font-family: 'Rajdhani', sans-serif; letter-spacing: 1px;
  box-shadow: 4px 4px 10px rgba(0,0,0,0.38), -2px -2px 5px rgba(255,255,255,0.038),
              inset 0 1px 0 rgba(255,255,255,0.07);
  transition: all 0.3s ease; cursor: default;
}
.feature-pill:hover {
  border-color: var(--c1); color: var(--c1);
  box-shadow: 4px 4px 10px rgba(0,0,0,0.38), -2px -2px 5px rgba(255,255,255,0.038),
              inset 0 1px 0 rgba(255,255,255,0.07), 0 0 14px rgba(0,245,212,0.28);
  transform: translateY(-3px);
}

/* === PROFILE CARDS === */
.p-card {
  width: 200px; text-align: center; cursor: pointer;
  background: linear-gradient(155deg,
    rgba(255,255,255,0.075) 0%,
    rgba(0,245,212,0.038) 50%,
    rgba(123,47,255,0.038) 100%);
  border: 1.5px solid rgba(255,255,255,0.13);
  border-radius: 28px; padding: 26px;
  box-shadow:
    9px 9px 26px rgba(0,0,0,0.55),
    -5px -5px 14px rgba(255,255,255,0.038),
    inset 0 2px 2px rgba(255,255,255,0.09),
    inset 0 -2px 2px rgba(0,0,0,0.28);
  transition: all 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative; overflow: hidden; backdrop-filter: blur(16px);
}
.p-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 50%;
  background: linear-gradient(180deg, rgba(255,255,255,0.065) 0%, transparent 100%);
  border-radius: 28px 28px 0 0; pointer-events: none;
}
.p-card:hover {
  transform: scale(1.13) translateY(-10px) rotate(-1.2deg);
  border-color: rgba(0,245,212,0.52);
  box-shadow:
    12px 12px 42px rgba(0,0,0,0.65), -5px -5px 14px rgba(255,255,255,0.045),
    0 0 35px rgba(0,245,212,0.22), inset 0 2px 2px rgba(255,255,255,0.11);
}
.p-img {
  width: 120px; height: 120px; border-radius: 50%; object-fit: cover;
  border: 3px solid rgba(0,245,212,0.32);
  box-shadow: 0 6px 20px rgba(0,0,0,0.5), 0 0 0 5px rgba(0,245,212,0.055),
              inset 0 2px 4px rgba(255,255,255,0.09);
  transition: all 0.4s ease;
}
.p-card:hover .p-img {
  border-color: var(--c1);
  box-shadow: 0 6px 20px rgba(0,0,0,0.5), 0 0 22px rgba(0,245,212,0.42), 0 0 0 6px rgba(0,245,212,0.09);
}
.p-name {
  margin-top: 14px; font-family: 'Orbitron', monospace; font-size: 0.8rem;
  color: rgba(255,255,255,0.62); letter-spacing: 2px; transition: color 0.3s;
}
.p-card:hover .p-name { color: var(--c1); }
.p-role { font-size: 0.7rem; color: rgba(255,255,255,0.30); margin-top: 4px; }

/* === BUTTONS === */
.stButton > button {
  font-family: 'Orbitron', monospace !important; font-size: 0.8rem !important;
  background: linear-gradient(145deg, #7b2fff, #00f5d4) !important;
  border: none !important; border-radius: 14px !important;
  color: #000 !important; font-weight: 800 !important;
  padding: 12px 30px !important; letter-spacing: 2.5px !important;
  text-transform: uppercase !important;
  box-shadow:
    0 6px 22px rgba(0,245,212,0.32),
    0 2px 0 rgba(255,255,255,0.18) inset,
    0 -2px 0 rgba(0,0,0,0.28) inset,
    4px 4px 12px rgba(0,0,0,0.38) !important;
  transition: all 0.25s cubic-bezier(0.175,0.885,0.32,1.275) !important;
  position: relative !important; overflow: hidden !important;
}
.stButton > button:hover {
  transform: translateY(-4px) scale(1.04) !important;
  box-shadow:
    0 12px 36px rgba(0,245,212,0.5), 0 0 50px rgba(123,47,255,0.28),
    0 2px 0 rgba(255,255,255,0.22) inset, 0 -2px 0 rgba(0,0,0,0.28) inset !important;
}
.stButton > button:active {
  transform: translateY(1px) scale(0.98) !important;
  box-shadow: 0 2px 8px rgba(0,245,212,0.28), 0 1px 0 rgba(255,255,255,0.12) inset !important;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
  background: rgba(0,5,16,0.52) !important;
  backdrop-filter: blur(35px) saturate(158%) !important;
  -webkit-backdrop-filter: blur(35px) saturate(158%) !important;
  border-right: 1px solid rgba(255,255,255,0.09) !important;
  box-shadow: inset -4px 0 30px rgba(0,0,0,0.48), 0 0 60px rgba(0,245,212,0.025) !important;
}
section[data-testid="stSidebar"] > div { padding: 20px; }
.sidebar-title {
  font-family: 'Orbitron', monospace; font-size: 0.88rem;
  letter-spacing: 2.5px; color: var(--c1); margin-bottom: 12px;
  text-shadow: 0 0 10px rgba(0,245,212,0.5);
}
.sidebar-card {
  background: linear-gradient(158deg, rgba(255,255,255,0.055) 0%, rgba(0,0,0,0.22) 100%);
  border-radius: 18px; padding: 16px 18px; margin-bottom: 14px;
  border: 1px solid rgba(255,255,255,0.09);
  box-shadow:
    5px 5px 14px rgba(0,0,0,0.52), -3px -3px 8px rgba(255,255,255,0.038),
    inset 0 1px 1px rgba(255,255,255,0.075);
  transition: all 0.3s ease;
}
.sidebar-card:hover {
  border-color: rgba(0,245,212,0.28);
  box-shadow: 5px 5px 14px rgba(0,0,0,0.52), -3px -3px 8px rgba(255,255,255,0.038),
              inset 0 1px 1px rgba(255,255,255,0.075), 0 0 16px rgba(0,245,212,0.09);
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.028);
  border-radius: 18px; border: 1px solid rgba(255,255,255,0.075);
  padding: 6px; gap: 3px; flex-wrap: wrap;
  box-shadow: inset 3px 3px 8px rgba(0,0,0,0.38), inset -2px -2px 5px rgba(255,255,255,0.038);
}
.stTabs [data-baseweb="tab"] {
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 0.8rem !important; letter-spacing: 1px !important;
  text-transform: uppercase !important; color: rgba(255,255,255,0.42) !important;
  border-radius: 12px !important; padding: 9px 12px !important; transition: all 0.25s ease !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(0,245,212,0.16), rgba(123,47,255,0.10)) !important;
  color: var(--c1) !important; border: 1px solid rgba(0,245,212,0.32) !important;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.38), -1px -1px 3px rgba(255,255,255,0.045),
              0 0 12px rgba(0,245,212,0.18) !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--c1) !important; background: rgba(0,245,212,0.065) !important;
}

/* === INSIGHT CARDS === */
.insight-card {
  background: linear-gradient(135deg, rgba(0,245,212,0.055) 0%, rgba(123,47,255,0.038) 100%);
  border: 1px solid rgba(0,245,212,0.13); border-left: 4px solid var(--c1);
  border-radius: 16px; padding: 18px 20px; margin-bottom: 12px;
  box-shadow: 4px 4px 14px rgba(0,0,0,0.38), -2px -2px 6px rgba(255,255,255,0.028),
              inset 0 1px 0 rgba(255,255,255,0.065);
  transition: all 0.3s ease; position: relative; overflow: hidden;
}
.insight-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, var(--c1), transparent);
}
.insight-card:hover {
  transform: translateX(5px); border-color: rgba(0,245,212,0.38);
  box-shadow: 6px 6px 20px rgba(0,0,0,0.48), var(--glow-cyan);
}
.insight-icon { font-size: 1.3rem; margin-right: 10px; }
.insight-text { font-size: 0.93rem; color: rgba(255,255,255,0.86); }

/* === MISC === */
.stDataFrame {
  border-radius: 14px; overflow: hidden;
  border: 1px solid rgba(255,255,255,0.09) !important;
  box-shadow: 4px 4px 14px rgba(0,0,0,0.38);
}
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3)) !important;
  border-radius: 4px !important; box-shadow: 0 0 10px rgba(0,245,212,0.48) !important;
}
.stTextInput > div > div > input {
  background: linear-gradient(145deg, rgba(255,255,255,0.038), rgba(0,0,0,0.18)) !important;
  border: 1px solid rgba(255,255,255,0.11) !important; border-radius: 12px !important;
  color: white !important; font-family: 'Rajdhani', sans-serif !important;
  box-shadow: inset 2px 2px 6px rgba(0,0,0,0.38), inset -1px -1px 3px rgba(255,255,255,0.038) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--c1) !important;
  box-shadow: inset 2px 2px 6px rgba(0,0,0,0.38), 0 0 12px rgba(0,245,212,0.38) !important;
}
header[data-testid="stHeader"] {
  background: rgba(0,5,16,0.72) !important;
  backdrop-filter: blur(22px) !important;
  border-bottom: 1px solid rgba(255,255,255,0.065) !important;
  box-shadow: 0 2px 20px rgba(0,0,0,0.48) !important;
}
#MainMenu, footer, .stDeployButton { visibility: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #000510; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(var(--c1), var(--c2)); border-radius: 4px;
  box-shadow: 0 0 6px rgba(0,245,212,0.38);
}
.clay-divider {
  height: 2px; border: none; margin: 20px 0;
  background: linear-gradient(90deg, transparent, var(--c1), var(--c2), var(--c3), transparent);
  border-radius: 2px; box-shadow: 0 0 10px rgba(0,245,212,0.38);
  animation: divGlow 3s ease-in-out infinite alternate;
}
@keyframes divGlow {
  0%   { box-shadow: 0 0 5px rgba(0,245,212,0.28); opacity:0.65; }
  100% { box-shadow: 0 0 18px rgba(0,245,212,0.68); opacity:1;   }
}
.signout-btn {
  background: linear-gradient(145deg, #ff006e, #7b2fff);
  border-radius: 14px; padding: 11px 18px;
  text-align: center; color: white; font-weight: bold;
  font-family: 'Orbitron', monospace; font-size: 0.76rem; letter-spacing: 2px;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(255,0,110,0.48), 4px 4px 10px rgba(0,0,0,0.48),
              inset 0 1px 0 rgba(255,255,255,0.13);
  transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY TEMPLATE ──────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Rajdhani, sans-serif", color="rgba(255,255,255,0.8)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)"),
    colorway=["#00f5d4","#7b2fff","#ff006e","#fb5607","#ffbe0b","#3a86ff"],
)
def styled_fig(fig):
    fig.update_layout(**PLOTLY_TEMPLATE, margin=dict(l=20,r=20,t=50,b=20))
    return fig

@st.cache_data
def load_data():
    df = pd.read_csv("ev_charging_dataset.csv")
    df.drop_duplicates(subset="Station ID", inplace=True)
    df["Renewable Energy Source"] = df["Renewable Energy Source"].fillna("Unknown")
    df["Reviews (Rating)"] = df["Reviews (Rating)"].fillna(df["Reviews (Rating)"].median())
    df["Connector Types"] = df["Connector Types"].fillna("Unknown")
    le = LabelEncoder()
    df["ChargerType_enc"] = le.fit_transform(df["Charger Type"])
    df["Renewable_enc"]   = (df["Renewable Energy Source"] == "Yes").astype(int)
    df["Maintenance_enc"] = le.fit_transform(df["Maintenance Frequency"])
    return df

def metric_card(col, val, label):
    col.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div>'
                 f'<div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

def section_title(icon, text):
    st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)

def clay_divider():
    st.markdown('<hr class="clay-divider">', unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "splash"

# ════════════════════════════════════════════════════════════════════════════
# SPLASH
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "splash":
    st.markdown("""
    <div class="splash-wrap">
      <div class="pulse-ring">⚡</div>
      <div class="splash-logo">SMARTCHARGE AI</div>
      <div class="splash-sub">▶ INITIALIZING EV INTELLIGENCE ENGINE...</div>
    </div>""", unsafe_allow_html=True)
    bar = st.progress(0)
    status = st.empty()
    steps = [
        ("🔌 Connecting to charging network...", "#00f5d4"),
        ("📡 Loading station telemetry...",      "#00f5d4"),
        ("🧠 Warming up ML models...",            "#7b2fff"),
        ("🗺️  Mapping global infrastructure...",  "#ff006e"),
        ("✅ Ready for launch!",                   "#00f5d4"),
    ]
    for i in range(101):
        bar.progress(i)
        idx = min(i // 22, 4)
        msg, col = steps[idx]
        status.markdown(
            f'<p style="text-align:center;font-family:Share Tech Mono;color:{col};'
            f'font-size:0.88rem;letter-spacing:3px;">{msg}</p>', unsafe_allow_html=True)
        time.sleep(0.015)
    st.session_state.page = "landing"
    st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# LANDING
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="hero-wrapper">
      <div class="hero-badge">⚡ AI-POWERED ANALYTICS PLATFORM v2.0</div>
      <div class="hero-title">SmartCharge<br>Intelligence</div>
      <div class="hero-sub">Decoding the future of EV charging infrastructure</div>
      <div class="feature-strip">
        <div class="feature-pill">🔍 Behavior Clustering</div>
        <div class="feature-pill">⚠️ Anomaly Detection</div>
        <div class="feature-pill">🔗 Association Mining</div>
        <div class="feature-pill">🌍 Geo Visualization</div>
        <div class="feature-pill">📈 Demand Forecasting</div>
        <div class="feature-pill">🤖 Machine Learning</div>
      </div>
    </div>""", unsafe_allow_html=True)
    _, c_m, _ = st.columns([1.2, 1, 1.2])
    with c_m:
        if st.button("⚡  LAUNCH DASHBOARD"):
            st.session_state.page = "profiles"; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    clay_divider()
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metric_card(c1, "5,000+", "Charging Stations")
    metric_card(c2, "20+",    "Global Cities")
    metric_card(c3, "6",      "ML Algorithms")
    metric_card(c4, "17",     "Data Dimensions")
    st.markdown("<br>", unsafe_allow_html=True)
    fa, fb, fc = st.columns(3)
    for col, (icon, title, desc) in zip([fa,fb,fc], [
        ("🧠","Smart Clustering","K-Means groups stations by behavior — daily commuters to premium fast-chargers."),
        ("⚡","Anomaly Detection","Z-score detection flags faulty stations, overloaded circuits, and billing irregularities."),
        ("🔗","Association Mining","FP-Growth uncovers hidden links between charger type, location, cost, and demand."),
    ]):
        with col:
            col.markdown(f"""
            <div class="liquid-glass" style="text-align:center;min-height:155px;">
              <div style="font-size:2.1rem;margin-bottom:10px;">{icon}</div>
              <div style="font-family:Orbitron,monospace;font-size:0.78rem;color:#00f5d4;
                          letter-spacing:2px;margin-bottom:7px;">{title.upper()}</div>
              <div style="font-size:0.86rem;color:rgba(255,255,255,0.58);">{desc}</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PROFILES
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "profiles":
    st.markdown("""
    <div style="text-align:center;padding-top:48px;animation:pageSlideIn 0.7s ease both;">
      <h1>Who's Analyzing Today?</h1>
      <p style="font-family:Share Tech Mono;color:rgba(255,255,255,0.32);
                letter-spacing:3px;font-size:0.78rem;">SELECT YOUR PROFILE TO CONTINUE</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    profiles = [
        ("https://cdn-icons-png.flaticon.com/512/3135/3135715.png",  "JASHITH",     "Data Scientist","Enter"),
        ("https://cdn-icons-png.flaticon.com/512/4140/4140048.png",  "ANALYST",     "Infra Lead",    "Enter"),
        ("https://cdn-icons-png.flaticon.com/512/1828/1828817.png","ADD PROFILE","New User","Create"),
    ]
    cols = st.columns(3)
    for i, (img, name, role, lbl) in enumerate(profiles):
        with cols[i]:
            st.markdown(f"""
            <div class="p-card" style="margin:0 auto;animation:staggerUp 0.5s {0.1*i+0.1:.1f}s ease both;">
              <img src="{img}" class="p-img"/>
              <div class="p-name">{name}</div>
              <div class="p-role">{role}</div>
            </div><br>""", unsafe_allow_html=True)
            if st.button(lbl, key=f"prof_{i}"):
                st.session_state.page = "dashboard" if i < 2 else "signup"
                st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# SIGNUP
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "signup":
    st.markdown("<h1 style='text-align:center;animation:pageSlideIn 0.6s ease both;'>Create Profile</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="clay-card">', unsafe_allow_html=True)
        name = st.text_input("👤 Name"); email = st.text_input("📧 Email")
        password = st.text_input("🔐 Password", type="password")
        if st.button("CREATE ACCOUNT ⚡"):
            st.session_state.otp = random.randint(100000,999999)
            st.session_state.page = "verify"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# OTP
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "verify":
    st.markdown("<h1 style='text-align:center;'>Email Verification</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        st.info("🔐 Demo Mode — Your OTP:")
        st.markdown(f'<div class="metric-val" style="text-align:center;font-size:2.6rem;">'
                    f'{st.session_state.get("otp","")}</div>', unsafe_allow_html=True)
        user_otp = st.text_input("Enter OTP")
        if st.button("VERIFY ⚡"):
            if str(user_otp) == str(st.session_state.get("otp","")):
                st.session_state.page = "dashboard"; st.rerun()
            else: st.error("❌ Invalid OTP.")
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "dashboard":

    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚡ SMART PANEL</div>', unsafe_allow_html=True)
        clay_divider()
        st.markdown("""
        <div class="sidebar-card">
          <div style="font-family:Orbitron,monospace;font-size:0.76rem;color:#00f5d4;letter-spacing:2px;margin-bottom:6px;">👤 ANALYST</div>
          <div style="font-size:0.8rem;color:rgba(255,255,255,0.48);">EV Intelligence User</div>
          <div style="font-size:0.72rem;color:rgba(255,255,255,0.28);margin-top:5px;">🟢 Online · Session Active</div>
        </div>
        <div class="sidebar-card">
          <div style="font-family:Orbitron,monospace;font-size:0.76rem;color:#00f5d4;letter-spacing:2px;margin-bottom:8px;">📊 NAVIGATION</div>
          <div style="font-size:0.83rem;color:rgba(255,255,255,0.55);line-height:2.0;">
            ⚡ Overview<br>🧹 Data Prep<br>📊 Usage<br>💰 Cost & Ops<br>📈 EDA<br>🔗 Correlation<br>🤖 Clustering<br>⚠️ Anomalies<br>💡 Insights
          </div>
        </div>
        <div class="sidebar-card">
          <div style="font-family:Orbitron,monospace;font-size:0.76rem;color:#00f5d4;letter-spacing:2px;margin-bottom:8px;">📈 LIVE STATS</div>
          <div style="font-size:0.8rem;color:rgba(255,255,255,0.52);line-height:1.9;">
            🔋 5,000 Stations<br>🌍 20 Cities<br>🤖 K=4 Clusters<br>⚠️ ~2–4% Anomalies
          </div>
        </div>""", unsafe_allow_html=True)
        clay_divider()
        if st.button("🚪 SIGN OUT", key="logout_btn"):
            st.session_state.page = "landing"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding-top:16px;animation:pageSlideIn 0.7s ease both;">
      <h1>⚡ SmartCharge Analytics</h1>
      <p style="font-family:Share Tech Mono;color:rgba(255,255,255,0.32);font-size:0.76rem;letter-spacing:4px;margin-bottom:0;">
        AI-POWERED EV INFRASTRUCTURE INTELLIGENCE PLATFORM</p>
    </div>""", unsafe_allow_html=True)
    clay_divider()

    df = load_data()

    tabs = st.tabs([
        "🏠 Overview","🧹 Data Prep","📊 Usage","💰 Cost & Ops",
        "📈 EDA Deep","🔗 Correlation","🤖 Clustering",
        "⛏️ Assoc Rules","⚠️ Anomalies","💡 Insights"
    ])

    # ── TAB 1: OVERVIEW ───────────────────────────────────────────────────────
    with tabs[0]:
        section_title("🌐","GLOBAL STATION OVERVIEW")
        c1,c2,c3,c4,c5 = st.columns(5)
        metric_card(c1, f"{len(df):,}", "Total Stations")
        metric_card(c2, df["Station Operator"].nunique(), "Operators")
        metric_card(c3, df["Charger Type"].nunique(), "Charger Types")
        metric_card(c4, f"{df['Usage Stats (avg users/day)'].mean():.1f}", "Avg Users/Day")
        metric_card(c5, f"{df['Reviews (Rating)'].mean():.2f}⭐", "Avg Rating")
        st.markdown("<br>", unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🗺️","GLOBAL STATION MAP")
            fig_map = px.scatter_mapbox(
                df.sample(min(1000,len(df))), lat="Latitude", lon="Longitude",
                color="Charger Type", size="Usage Stats (avg users/day)",
                hover_name="Address", hover_data=["Cost (USD/kWh)","Reviews (Rating)"],
                mapbox_style="carto-darkmatter", zoom=1, height=420,
                color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"})
            fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_map, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("🔌","CHARGER TYPE DISTRIBUTION")
            ct = df["Charger Type"].value_counts().reset_index(); ct.columns=["Type","Count"]
            fig_pie = px.pie(ct, names="Type", values="Count", hole=0.6,
                             color_discrete_sequence=["#00f5d4","#7b2fff","#ff006e"])
            fig_pie = styled_fig(fig_pie); fig_pie.update_traces(textfont_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
            section_title("♻️","RENEWABLE ENERGY SPLIT")
            re = df["Renewable Energy Source"].value_counts().reset_index(); re.columns=["Source","Count"]
            fig_re = px.bar(re, x="Source", y="Count", color="Source",
                            color_discrete_sequence=["#00f5d4","#7b2fff","#ff006e"])
            fig_re = styled_fig(fig_re)
            st.plotly_chart(fig_re, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
        section_title("📋","RAW DATASET PREVIEW")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: DATA PREP ──────────────────────────────────────────────────────
    with tabs[1]:
        section_title("🧹","DATA CLEANING & PREPROCESSING")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("❓","MISSING VALUES ANALYSIS")
            mv = pd.DataFrame({"Column":df.columns,"Missing":df.isnull().sum().values,
                               "% Missing":(df.isnull().sum().values/len(df)*100).round(2)})
            fig_mv = px.bar(mv[mv["Missing"]>0], x="Column", y="% Missing",
                            color="% Missing", color_continuous_scale=["#00f5d4","#ff006e"])
            fig_mv = styled_fig(fig_mv); fig_mv.update_layout(title="Missing Value % by Column")
            st.plotly_chart(fig_mv, use_container_width=True)
            st.dataframe(mv, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("📐","NUMERIC FEATURE DISTRIBUTIONS")
            num_cols = ["Cost (USD/kWh)","Usage Stats (avg users/day)","Charging Capacity (kW)","Distance to City (km)"]
            fig_box = go.Figure()
            for c, color in zip(num_cols,["#00f5d4","#7b2fff","#ff006e","#fb5607"]):
                fig_box.add_trace(go.Box(y=df[c], name=c, marker_color=color, line_color=color))
            fig_box.update_layout(**PLOTLY_TEMPLATE, title="Box Plots: Key Numeric Features")
            st.plotly_chart(fig_box, use_container_width=True)
            section_title("🔢","ENCODING SUMMARY")
            enc_df = pd.DataFrame({
                "Feature":["Charger Type","Renewable Energy Source","Maintenance Frequency"],
                "Encoding":["Label Encoding (0,1,2)","Binary (0=No, 1=Yes)","Label Encoding"],
                "Uniques":[df["Charger Type"].nunique(),df["Renewable Energy Source"].nunique(),df["Maintenance Frequency"].nunique()]
            })
            st.dataframe(enc_df, use_container_width=True)
            st.success("✅ Duplicates removed · Missing values imputed · Features encoded")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 3: USAGE ──────────────────────────────────────────────────────────
    with tabs[2]:
        section_title("📊","USAGE PATTERNS & DEMAND ANALYSIS")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("📉","USAGE STATS DISTRIBUTION")
            fig_hist = px.histogram(df, x="Usage Stats (avg users/day)", nbins=40,
                                    color_discrete_sequence=["#00f5d4"], marginal="violin")
            fig_hist = styled_fig(fig_hist); fig_hist.update_layout(title="Distribution of Daily Users per Station")
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("📅","USAGE GROWTH OVER INSTALLATION YEARS")
            yearly = df.groupby("Installation Year")["Usage Stats (avg users/day)"].mean().reset_index()
            fig_line = px.line(yearly, x="Installation Year", y="Usage Stats (avg users/day)",
                               markers=True, color_discrete_sequence=["#00f5d4"])
            fig_line.add_scatter(x=yearly["Installation Year"], y=yearly["Usage Stats (avg users/day)"],
                                 fill="tozeroy", fillcolor="rgba(0,245,212,0.06)", line_color="rgba(0,0,0,0)")
            fig_line = styled_fig(fig_line); fig_line.update_layout(title="Average Usage by Installation Year")
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("⚡","USAGE BY CHARGER TYPE")
            fig_box_ct = px.box(df, x="Charger Type", y="Usage Stats (avg users/day)", color="Charger Type",
                                color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"})
            fig_box_ct = styled_fig(fig_box_ct); fig_box_ct.update_layout(title="Usage Distribution by Charger Type")
            st.plotly_chart(fig_box_ct, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("♻️","RENEWABLE VS NON-RENEWABLE USAGE")
            re_usage = df.groupby("Renewable Energy Source")["Usage Stats (avg users/day)"].mean().reset_index()
            fig_re = px.bar(re_usage, x="Renewable Energy Source", y="Usage Stats (avg users/day)",
                            color="Renewable Energy Source",
                            color_discrete_sequence=["#00f5d4","#ff006e","#7b2fff"], text_auto=True)
            fig_re = styled_fig(fig_re); fig_re.update_layout(title="Avg Daily Users: Renewable vs Non-Renewable")
            st.plotly_chart(fig_re, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        section_title("🏙️","USAGE VS DISTANCE TO CITY")
        fig_s = px.scatter(df, x="Distance to City (km)", y="Usage Stats (avg users/day)",
                           color="Charger Type", size="Charging Capacity (kW)",
                           hover_name="Address", opacity=0.7,
                           color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"},
                           trendline="lowess")
        fig_s = styled_fig(fig_s); fig_s.update_layout(title="Station Usage vs Distance to City Center")
        st.plotly_chart(fig_s, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4: COST & OPS ─────────────────────────────────────────────────────
    with tabs[3]:
        section_title("💰","COST & OPERATOR ANALYSIS")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🏢","COST DISTRIBUTION BY OPERATOR")
            fig_opbox = px.box(df, x="Station Operator", y="Cost (USD/kWh)", color="Station Operator")
            fig_opbox = styled_fig(fig_opbox); fig_opbox.update_layout(title="Charging Cost per Operator", showlegend=False)
            st.plotly_chart(fig_opbox, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("⭐","OPERATOR RATINGS VS USAGE")
            op_stats = df.groupby("Station Operator").agg(
                avg_rating=("Reviews (Rating)","mean"),
                avg_usage=("Usage Stats (avg users/day)","mean"),
                count=("Station ID","count")).reset_index()
            fig_op = px.scatter(op_stats, x="avg_rating", y="avg_usage", size="count",
                                color="Station Operator", text="Station Operator", size_max=40)
            fig_op = styled_fig(fig_op); fig_op.update_layout(title="Operator: Avg Rating vs Avg Usage")
            st.plotly_chart(fig_op, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("💲","COST VS USAGE DEMAND")
            fig_cv = px.scatter(df, x="Cost (USD/kWh)", y="Usage Stats (avg users/day)",
                                color="Charger Type", opacity=0.6, trendline="ols",
                                color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"})
            fig_cv = styled_fig(fig_cv); fig_cv.update_layout(title="Does Cost Affect Usage?")
            st.plotly_chart(fig_cv, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🔧","MAINTENANCE FREQUENCY & RATINGS")
            maint = df.groupby("Maintenance Frequency")["Reviews (Rating)"].mean().reset_index()
            fig_maint = px.bar(maint, x="Maintenance Frequency", y="Reviews (Rating)",
                               color="Maintenance Frequency", text_auto=".2f")
            fig_maint = styled_fig(fig_maint); fig_maint.update_layout(title="Rating by Maintenance Frequency", showlegend=False)
            st.plotly_chart(fig_maint, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 5: EDA DEEP DIVE ──────────────────────────────────────────────────
    with tabs[4]:
        section_title("📈","EXPLORATORY DATA ANALYSIS — DEEP DIVE")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🏙️","TOP 10 CITIES BY AVG USAGE")
            df["City"] = df["Address"].str.extract(r', ([A-Za-z\s]+),')[0].str.strip()
            city_usage = df.groupby("City")["Usage Stats (avg users/day)"].mean().nlargest(10).reset_index()
            fig_city = px.bar(city_usage, x="Usage Stats (avg users/day)", y="City",
                              orientation="h", color="Usage Stats (avg users/day)",
                              color_continuous_scale=["#7b2fff","#00f5d4"])
            fig_city = styled_fig(fig_city); fig_city.update_layout(title="Top Cities by Average Daily Usage")
            st.plotly_chart(fig_city, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("⭐","RATING DISTRIBUTION")
            fig_rat = px.histogram(df, x="Reviews (Rating)", nbins=20,
                                   color_discrete_sequence=["#7b2fff"], marginal="rug")
            fig_rat = styled_fig(fig_rat); fig_rat.update_layout(title="Distribution of Station Ratings")
            st.plotly_chart(fig_rat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("🅿️","PARKING SPOTS VS USAGE")
            fig_park = px.scatter(df, x="Parking Spots", y="Usage Stats (avg users/day)",
                                  color="Charger Type", opacity=0.6, trendline="ols",
                                  color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"})
            fig_park = styled_fig(fig_park); fig_park.update_layout(title="Parking Spots vs Station Usage")
            st.plotly_chart(fig_park, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🔋","CHARGING CAPACITY DISTRIBUTION")
            cap_counts = df["Charging Capacity (kW)"].value_counts().reset_index()
            cap_counts.columns = ["Capacity (kW)","Count"]
            fig_cap = px.bar(cap_counts, x="Capacity (kW)", y="Count",
                             color="Count", color_continuous_scale=["#7b2fff","#00f5d4"])
            fig_cap = styled_fig(fig_cap); fig_cap.update_layout(title="Station Count by Charging Capacity")
            st.plotly_chart(fig_cap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        section_title("🌡️","USAGE HEATMAP: CHARGER TYPE × AVAILABILITY")
        pivot = df.pivot_table(index="Charger Type", columns="Availability",
                               values="Usage Stats (avg users/day)", aggfunc="mean")
        fig_hm = px.imshow(pivot, color_continuous_scale=["#000510","#7b2fff","#00f5d4"],
                           aspect="auto", text_auto=".1f")
        fig_hm = styled_fig(fig_hm); fig_hm.update_layout(title="Average Usage by Charger Type and Availability Window")
        st.plotly_chart(fig_hm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 6: CORRELATION ────────────────────────────────────────────────────
    with tabs[5]:
        section_title("🔗","FEATURE CORRELATION ANALYSIS")
        col1,col2 = st.columns([3,2])
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🌡️","CORRELATION HEATMAP")
            num_df = df.select_dtypes(include="number").drop(columns=["Latitude","Longitude"], errors="ignore")
            corr = num_df.corr()
            fig_corr = px.imshow(corr, color_continuous_scale=["#ff006e","#000510","#00f5d4"],
                                 zmin=-1, zmax=1, text_auto=".2f", aspect="auto", height=500)
            fig_corr = styled_fig(fig_corr); fig_corr.update_layout(title="Pearson Correlation Matrix")
            st.plotly_chart(fig_corr, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("📊","TOP CORRELATED PAIRS")
            corr_pairs = corr.unstack().reset_index()
            corr_pairs.columns = ["Feature A","Feature B","Correlation"]
            corr_pairs = corr_pairs[corr_pairs["Feature A"] != corr_pairs["Feature B"]]
            corr_pairs["abs_corr"] = corr_pairs["Correlation"].abs()
            top_corr = corr_pairs.nlargest(12,"abs_corr")
            fig_tc = px.bar(top_corr, x="abs_corr",
                            y=top_corr["Feature A"]+"→"+top_corr["Feature B"],
                            color="Correlation", color_continuous_scale=["#ff006e","#7b2fff","#00f5d4"],
                            orientation="h")
            fig_tc = styled_fig(fig_tc); fig_tc.update_layout(title="Strongest Feature Correlations", height=500)
            st.plotly_chart(fig_tc, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
        section_title("🔍","SCATTER MATRIX — KEY FEATURES")
        fig_spm = px.scatter_matrix(df.sample(500),
            dimensions=["Cost (USD/kWh)","Usage Stats (avg users/day)",
                        "Charging Capacity (kW)","Reviews (Rating)","Distance to City (km)"],
            color="Charger Type", opacity=0.5,
            color_discrete_map={"DC Fast Charger":"#00f5d4","AC Level 2":"#7b2fff","AC Level 1":"#ff006e"})
        fig_spm = styled_fig(fig_spm); fig_spm.update_layout(title="Scatter Matrix of Key Features", height=600)
        st.plotly_chart(fig_spm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 7: CLUSTERING ─────────────────────────────────────────────────────
    with tabs[6]:
        section_title("🤖","CHARGING STATION CLUSTERING")
        features = ["Cost (USD/kWh)","Charging Capacity (kW)","Usage Stats (avg users/day)","Distance to City (km)","Reviews (Rating)"]
        scaler = StandardScaler()
        scaled = scaler.fit_transform(df[features].fillna(0))
        col1,col2 = st.columns([2,1])
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("📐","ELBOW METHOD — OPTIMAL K")
            inertias = []
            for k in range(2,12):
                km = KMeans(n_clusters=k, random_state=42, n_init=10); km.fit(scaled); inertias.append(km.inertia_)
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(x=list(range(2,12)), y=inertias, mode="lines+markers",
                                           line=dict(color="#00f5d4",width=3),
                                           marker=dict(color="#7b2fff",size=10,line=dict(color="#00f5d4",width=2))))
            fig_elbow.add_vline(x=4, line_dash="dash", line_color="#ff006e", annotation_text="Optimal K=4")
            fig_elbow.update_layout(**PLOTLY_TEMPLATE, title="Elbow Method", xaxis_title="K", yaxis_title="Inertia")
            st.plotly_chart(fig_elbow, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass" style="height:100%;">', unsafe_allow_html=True)
            section_title("🏷️","CLUSTER LABELS")
            for c, label, sub in [
                ("#00f5d4","Cluster 0 — Daily Commuters","Moderate use, low cost"),
                ("#7b2fff","Cluster 1 — Heavy Fast-Chargers","High capacity, high demand"),
                ("#ff006e","Cluster 2 — Occasional Users","Low frequency, rural"),
                ("#fb5607","Cluster 3 — Premium Stations","High cost, high ratings"),
            ]:
                st.markdown(f'<div class="insight-card"><b style="color:{c};">{label}</b>'
                            f'<br><small style="color:rgba(255,255,255,0.42);">{sub}</small></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(scaled)
        cluster_names = {0:"Daily Commuters",1:"Heavy Fast-Chargers",2:"Occasional Users",3:"Premium Stations"}
        df["Cluster Label"] = df["Cluster"].map(cluster_names)

        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("⚡","CLUSTERS: CAPACITY VS USAGE")
            fig_cl = px.scatter(df, x="Charging Capacity (kW)", y="Usage Stats (avg users/day)",
                                color="Cluster Label", size="Cost (USD/kWh)",
                                hover_name="Address", opacity=0.75,
                                color_discrete_sequence=["#00f5d4","#7b2fff","#ff006e","#fb5607"])
            fig_cl = styled_fig(fig_cl); fig_cl.update_layout(title="Station Clusters by Capacity & Demand")
            st.plotly_chart(fig_cl, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🗺️","CLUSTER MAP")
            fig_cmap = px.scatter_mapbox(
                df.sample(min(800,len(df))), lat="Latitude", lon="Longitude",
                color="Cluster Label", hover_name="Address",
                mapbox_style="carto-darkmatter", zoom=1, height=380,
                color_discrete_sequence=["#00f5d4","#7b2fff","#ff006e","#fb5607"])
            fig_cmap.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_cmap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        section_title("📊","CLUSTER RADAR PROFILE")
        cluster_profile = df.groupby("Cluster Label")[features].mean().reset_index()
        colors = ["#00f5d4","#7b2fff","#ff006e","#fb5607"]
        fig_radar = go.Figure()
        for i, row in cluster_profile.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=row[features].values.tolist() + [row[features[0]]],
                theta=features + [features[0]], fill="toself",
                name=row["Cluster Label"], line_color=colors[i],
                fillcolor=hex_to_rgba(colors[i], 0.10)))
        fig_radar.update_layout(**PLOTLY_TEMPLATE,
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.07)")),
            title="Cluster Profiles (Radar)", height=460)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 8: ASSOCIATION RULES ──────────────────────────────────────────────
    with tabs[7]:
        section_title("⛏️","ASSOCIATION RULE MINING")
        try:
            from mlxtend.frequent_patterns import apriori, association_rules as arm
            num_df_arm = df.select_dtypes(include="number").drop(
                columns=["Latitude","Longitude","Cluster"], errors="ignore").fillna(0)
            binary = (num_df_arm > num_df_arm.mean()).astype(bool)
            freq   = apriori(binary, min_support=0.1, use_colnames=True)
            rules  = arm(freq, metric="lift", min_threshold=1.0)
            rules["antecedents"] = rules["antecedents"].apply(lambda x:", ".join(list(x)))
            rules["consequents"] = rules["consequents"].apply(lambda x:", ".join(list(x)))
            col1,col2 = st.columns(2)
            with col1:
                st.markdown('<div class="clay-card">', unsafe_allow_html=True)
                section_title("📊","SUPPORT VS CONFIDENCE")
                fig_ar = px.scatter(rules, x="support", y="confidence", color="lift",
                                    size="lift", hover_data=["antecedents","consequents"],
                                    color_continuous_scale=["#7b2fff","#00f5d4","#ff006e"], size_max=25)
                fig_ar = styled_fig(fig_ar); fig_ar.update_layout(title="Rules: Support vs Confidence vs Lift")
                st.plotly_chart(fig_ar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
                section_title("🔝","TOP RULES BY LIFT")
                top_rules = rules.nlargest(10,"lift")[["antecedents","consequents","support","confidence","lift"]]
                fig_lift = px.bar(top_rules, x="lift",
                                  y=top_rules["antecedents"]+" → "+top_rules["consequents"],
                                  color="confidence", orientation="h",
                                  color_continuous_scale=["#7b2fff","#00f5d4"])
                fig_lift = styled_fig(fig_lift); fig_lift.update_layout(title="Top 10 Association Rules by Lift")
                st.plotly_chart(fig_lift, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("📋","FULL RULES TABLE")
            st.dataframe(rules[["antecedents","consequents","support","confidence","lift"]].round(4).head(30), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Association rules error: {e}")

    # ── TAB 9: ANOMALY DETECTION ──────────────────────────────────────────────
    with tabs[8]:
        section_title("⚠️","ANOMALY DETECTION")
        num_cols_anom = df.select_dtypes(include="number").drop(
            columns=["Latitude","Longitude","Cluster"], errors="ignore").fillna(0)
        z_scores = np.abs(zscore(num_cols_anom))
        df["Anomaly"] = (z_scores > 3).any(axis=1)
        df["Max_Z"]   = z_scores.max(axis=1)
        n_anom = int(df["Anomaly"].sum()); a_pct = n_anom/len(df)*100
        c1,c2,c3 = st.columns(3)
        metric_card(c1, f"{n_anom:,}", "Anomalous Stations")
        metric_card(c2, f"{a_pct:.1f}%", "Anomaly Rate")
        metric_card(c3, f"{df['Max_Z'].max():.2f}", "Max Z-Score")
        st.markdown("<br>", unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🔍","ANOMALY SCATTER: COST VS USAGE")
            fig_anom = px.scatter(df, x="Cost (USD/kWh)", y="Usage Stats (avg users/day)",
                                  color="Anomaly", symbol="Anomaly",
                                  color_discrete_map={True:"#ff006e",False:"rgba(0,245,212,0.4)"},
                                  hover_name="Address", size="Max_Z", size_max=20)
            fig_anom = styled_fig(fig_anom); fig_anom.update_layout(title="Anomalies: Cost vs Usage")
            st.plotly_chart(fig_anom, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("📊","Z-SCORE DISTRIBUTION")
            fig_z = px.histogram(df, x="Max_Z", nbins=50, color_discrete_sequence=["#7b2fff"])
            fig_z.add_vline(x=3, line_dash="dash", line_color="#ff006e", annotation_text="Anomaly Threshold (Z=3)")
            fig_z = styled_fig(fig_z); fig_z.update_layout(title="Distribution of Maximum Z-Scores")
            st.plotly_chart(fig_z, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("🗺️","ANOMALY MAP")
            df_anom_map = df[df["Anomaly"]].sample(min(200,n_anom))
            df_norm_map = df[~df["Anomaly"]].sample(min(400,(~df["Anomaly"]).sum()))
            df_plot = pd.concat([df_anom_map, df_norm_map])
            fig_amap = px.scatter_mapbox(df_plot, lat="Latitude", lon="Longitude", color="Anomaly",
                                         color_discrete_map={True:"#ff006e",False:"rgba(0,245,212,0.3)"},
                                         hover_name="Address", mapbox_style="carto-darkmatter", zoom=1, height=380)
            fig_amap.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_amap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("🏢","ANOMALIES BY OPERATOR")
            anom_by_op = df.groupby("Station Operator")["Anomaly"].sum().reset_index()
            anom_by_op.columns = ["Operator","Anomaly Count"]
            fig_aop = px.bar(anom_by_op, x="Operator", y="Anomaly Count",
                             color="Anomaly Count", color_continuous_scale=["#7b2fff","#ff006e"])
            fig_aop = styled_fig(fig_aop); fig_aop.update_layout(title="Anomalous Stations per Operator")
            st.plotly_chart(fig_aop, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        section_title("📋","DETECTED ANOMALIES TABLE")
        anomaly_df = df[df["Anomaly"]][["Station ID","Address","Charger Type","Cost (USD/kWh)",
                                        "Usage Stats (avg users/day)","Reviews (Rating)","Max_Z"]].round(3)
        st.dataframe(anomaly_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 10: INSIGHTS ──────────────────────────────────────────────────────
    with tabs[9]:
        section_title("💡","KEY INSIGHTS & FINDINGS")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("⚡","CHARGING BEHAVIOR")
            for icon, text in [
                ("🔋","<b>DC Fast Chargers</b> consistently attract the highest daily user volumes across all geographies."),
                ("🏙️","Stations <b>within 5km of city centers</b> see 2–3× more daily users than suburban counterparts."),
                ("♻️","<b>Renewable-powered stations</b> receive statistically higher ratings (avg +0.3⭐) and slightly higher usage."),
                ("📅","Stations installed after 2018 show a <b>sharp uptick in usage</b>, reflecting growing EV adoption."),
            ]:
                st.markdown(f'<div class="insight-card"><span class="insight-icon">{icon}</span>'
                            f'<span class="insight-text">{text}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
            section_title("💰","COST & OPERATOR INSIGHTS")
            for icon, text in [
                ("📉","<b>Lower-cost stations</b> near urban cores dominate daily demand — price sensitivity is real."),
                ("🏆","<b>ChargePoint & Tesla</b> lead on average ratings while EVgo and Ionity have wider pricing variance."),
                ("🔧","<b>Monthly maintenance</b> correlates with marginally better ratings vs annually maintained stations."),
                ("⚠️","Some operators show <b>high cost + low ratings</b> — a red flag for customer retention issues."),
            ]:
                st.markdown(f'<div class="insight-card"><span class="insight-icon">{icon}</span>'
                            f'<span class="insight-text">{text}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="skeuo-card">', unsafe_allow_html=True)
            section_title("🤖","CLUSTERING INSIGHTS")
            for icon, text in [
                ("🟢","<b>Daily Commuters (Cluster 0):</b> Medium cost, moderate usage — ideal for workplace charging incentives."),
                ("🟣","<b>Heavy Fast-Chargers (Cluster 1):</b> High capacity & demand — infrastructure bottlenecks likely here."),
                ("🔴","<b>Occasional Users (Cluster 2):</b> Rural, low frequency — may benefit from promotional pricing."),
                ("🟠","<b>Premium Stations (Cluster 3):</b> High cost, excellent ratings — target for loyalty programs."),
            ]:
                st.markdown(f'<div class="insight-card"><span class="insight-icon">{icon}</span>'
                            f'<span class="insight-text">{text}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="clay-card">', unsafe_allow_html=True)
            section_title("⚠️","ANOMALY FINDINGS")
            for icon, text in [
                ("🚨","Roughly <b>2–4% of stations</b> exhibit statistically anomalous behavior across cost, usage, and capacity."),
                ("🔴","Anomalous stations often show <b>high cost combined with below-average ratings</b> — possible faulty equipment."),
                ("📍","Anomalies are <b>geographically dispersed</b> with slight concentration in newer stations post-2020."),
                ("🔧","<b>Immediate inspection recommended</b> for stations with Z-score > 5 — these are extreme outliers."),
            ]:
                st.markdown(f'<div class="insight-card"><span class="insight-icon">{icon}</span>'
                            f'<span class="insight-text">{text}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        clay_divider()
        st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
        section_title("🎯","STRATEGIC RECOMMENDATIONS")
        recs = [
            ("🏗️","Infrastructure","Expand DC Fast Charger coverage within 5km of city centers — highest ROI zone for new installations."),
            ("💲","Pricing Strategy","Introduce dynamic pricing tied to demand. Low off-peak rates can redistribute load and improve utilization."),
            ("🔧","Maintenance","Prioritize monthly maintenance for high-usage clusters. Proactive servicing prevents anomaly escalation."),
            ("♻️","Sustainability","Transition stations to renewable sources — rated higher by users and differentiates premium offerings."),
            ("📊","Analytics","Deploy real-time Z-score monitoring. Automated alerts can flag faulty stations within hours."),
            ("📱","User Experience","Loyalty programs targeting 'Daily Commuter' clusters significantly improve utilization consistency."),
        ]
        r1,r2,r3 = st.columns(3)
        for i,(icon,title,text) in enumerate(recs):
            with [r1,r2,r3][i%3]:
                st.markdown(f"""
                <div class="skeuo-card" style="text-align:left;margin-bottom:14px;">
                  <div style="font-size:1.75rem;margin-bottom:7px;">{icon}</div>
                  <div style="font-family:Orbitron,monospace;font-size:0.72rem;color:#00f5d4;letter-spacing:2px;margin-bottom:5px;">{title.upper()}</div>
                  <div style="font-size:0.85rem;color:rgba(255,255,255,0.62);">{text}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    clay_divider()
    st.markdown("""
    <p style="text-align:center;font-family:Share Tech Mono;font-size:0.7rem;
              color:rgba(255,255,255,0.2);letter-spacing:3px;padding-bottom:20px;">
    ⚡ SMARTCHARGE AI · CLAY + SKEUO + LIQUID GLASS EDITION · © 2024
    </p>""", unsafe_allow_html=True)
