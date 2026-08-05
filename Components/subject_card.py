from html import escape

import streamlit as st


def _subject_card_styles():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.ta-subject-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03), 
                inset 0 2px 0 rgba(255, 255, 255, 0.7);
    padding: 24px;
    margin: 18px 0 14px;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.ta-subject-card:hover {
    transform: translateY(-4px) scale(1.005);
    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08), 
                0 5px 15px rgba(15, 23, 42, 0.03);
    border-color: rgba(99, 102, 241, 0.3);
}

.ta-subject-grid {
    display: grid;
    grid-template-columns: minmax(0, 7fr) minmax(220px, 3fr);
    gap: 24px;
    align-items: stretch;
}

.ta-subject-main {
    min-width: 0;
}

.ta-subject-kicker {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #6366f1;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.ta-subject-card .ta-subject-title,
.ta-subject-card h3.ta-subject-title {
    margin: 0;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a;
    font-family: "Sora", sans-serif;
    font-size: clamp(1.4rem, 2.2vw, 1.8rem);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.ta-subject-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 16px 0 20px;
}

.ta-subject-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 8px;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 0.78rem;
    font-weight: 650;
    padding: 6px 12px;
    border: 1px solid rgba(99, 102, 241, 0.15);
    transition: background 0.2s;
}

.ta-subject-badge:hover {
    background: #e0e7ff;
}

.ta-subject-badge span {
    color: #6b7280;
    font-weight: 500;
}

.ta-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
}

.ta-stat-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid rgba(226, 232, 240, 0.8);
    padding: 14px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
    transition: all 0.2s ease;
}

.ta-stat-card:hover {
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    border-color: rgba(203, 213, 225, 0.8);
}

.ta-stat-icon {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
    color: #4f46e5;
}

.ta-stat-icon .material-symbols-outlined {
    font-size: 20px;
    font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 24;
}

.ta-stat-value {
    color: #0f172a;
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.1;
}

.ta-stat-label {
    color: #64748b;
    font-size: 0.7rem;
    font-weight: 650;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    margin-top: 4px;
}

.ta-subject-side {
    display: flex;
    flex-direction: column;
    gap: 14px;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    padding: 20px;
}

.ta-instructor {
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    gap: 12px;
    align-items: center;
    padding-bottom: 14px;
    border-bottom: 1px dashed rgba(203, 213, 225, 0.8);
}

.ta-avatar {
    display: grid;
    place-items: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: #ffffff;
    font-size: 0.95rem;
    font-weight: 700;
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.25);
}

.ta-side-label {
    color: #64748b;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}

.ta-side-value {
    color: #0f172a;
    font-size: 0.95rem;
    font-weight: 700;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-top: 2px;
}

.ta-meta-list {
    display: grid;
    gap: 10px;
}

.ta-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    color: #64748b;
    font-size: 0.8rem;
}

.ta-meta-row strong {
    color: #1e293b;
    font-weight: 700;
}

.ta-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #166534;
    background: #dcfce7;
    border: 1px solid #bbf7d0;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 700;
}

.ta-status-pill::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22c55e;
}

@media (max-width: 760px) {
    .ta-subject-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _safe(value):
    return escape(str(value)) if value is not None else ""


def _initials(name):
    words = [word for word in str(name or "Instructor").split() if word]
    if not words:
        return "IN"
    return "".join(word[0].upper() for word in words[:2])


def _render_stat_cards(stats):
    if not stats:
        return ""

    cards = []
    for icon, label, value in stats:
        cards.append(
            '<div class="ta-stat-card">'
            f'<div class="ta-stat-icon"><span class="material-symbols-outlined">{_safe(icon)}</span></div>'
            '<div>'
            f'<div class="ta-stat-value">{_safe(value)}</div>'
            f'<div class="ta-stat-label">{_safe(label)}</div>'
            '</div>'
            '</div>'
        )
    return '<div class="ta-stat-grid">' + "".join(cards) + '</div>'


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None,
    actions=None,
    teacher_name=None,
):
    """
    Reusable subject card component.

    Args:
        name: Subject name
        code: Subject code
        section: Section identifier
        stats: List of (icon, label, value) tuples
        footer_callback: Callable to render footer buttons
        actions: List of (label, key, callback) tuples for action buttons
        teacher_name: Optional instructor name to show in the metadata rail
    """
    _subject_card_styles()

    instructor = teacher_name or "Assigned Instructor"
    html = (
        '<section class="ta-subject-card">'
        '<div class="ta-subject-grid">'
        '<div class="ta-subject-main">'
        '<div class="ta-subject-kicker"><span class="material-symbols-outlined" style="font-size:16px;">library_books</span> Subject</div>'
        '<h3 class="ta-subject-title" '
        'style="margin:0;color:#101828!important;-webkit-text-fill-color:#101828;'
        'font-family:Sora,sans-serif;font-size:1.55rem;font-weight:850;line-height:1.16;opacity:1;">'
        f'{_safe(name)}</h3>'
        '<div class="ta-subject-badges">'
        f'<div class="ta-subject-badge"><span>Code</span>{_safe(code)}</div>'
        f'<div class="ta-subject-badge"><span>Section</span>{_safe(section)}</div>'
        '</div>'
        f'{_render_stat_cards(stats)}'
        '</div>'
        '<aside class="ta-subject-side">'
        '<div class="ta-instructor">'
        f'<div class="ta-avatar">{_safe(_initials(instructor))}</div>'
        '<div>'
        '<div class="ta-side-label">Instructor</div>'
        f'<div class="ta-side-value">{_safe(instructor)}</div>'
        '</div>'
        '</div>'
        '<div class="ta-meta-list">'
        '<div class="ta-meta-row"><span>Status</span><strong><span class="ta-status-pill">Active</span></strong></div>'
        '<div class="ta-meta-row"><span>Last Class</span><strong>Not scheduled</strong></div>'
        '<div class="ta-meta-row"><span>Created</span><strong>Recently</strong></div>'
        '</div>'
        '</aside>'
        '</div>'
        '</section>'
    )

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

    if actions:
        cols = st.columns(len(actions))
        for i, (label, key, callback) in enumerate(actions):
            with cols[i]:
                if st.button(label, key=key):
                    callback()
