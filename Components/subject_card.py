from html import escape

import streamlit as st


def _subject_card_styles():
    st.markdown(
        """
<style>
.ta-subject-card {
    position: relative;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid rgba(75, 86, 148, 0.14);
    border-left: 6px solid #4B5694;
    border-radius: 18px;
    box-shadow: 0 18px 42px rgba(15, 23, 42, 0.08);
    padding: 24px;
    margin: 18px 0 14px;
}
.ta-subject-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    background: linear-gradient(90deg, #4B5694, rgba(75, 86, 148, 0.08));
}
.ta-subject-grid {
    display: grid;
    grid-template-columns: minmax(0, 7fr) minmax(220px, 3fr);
    gap: 22px;
    align-items: stretch;
}
.ta-subject-main {
    min-width: 0;
}
.ta-subject-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #4B5694;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ta-subject-card .ta-subject-title,
.ta-subject-card h3.ta-subject-title {
    margin: 0;
    color: #101828 !important;
    -webkit-text-fill-color: #101828;
    font-family: "Sora", sans-serif;
    font-size: clamp(1.28rem, 2.2vw, 1.7rem);
    font-weight: 850;
    line-height: 1.16;
    opacity: 1;
}
.ta-subject-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin: 14px 0 18px;
}
.ta-subject-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    border-radius: 999px;
    border: 1px solid rgba(75, 86, 148, 0.16);
    background: #F4F5FF;
    color: #4B5694;
    font-size: 0.78rem;
    font-weight: 750;
    padding: 7px 11px;
    line-height: 1;
}
.ta-subject-badge span {
    color: #64748b;
    font-weight: 700;
}
.ta-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(132px, 1fr));
    gap: 12px;
}
.ta-stat-card {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    align-items: center;
    gap: 11px;
    min-height: 74px;
    border-radius: 14px;
    border: 1px solid rgba(15, 23, 42, 0.08);
    background: linear-gradient(180deg, #ffffff 0%, #F8FAFC 100%);
    padding: 13px 14px;
}
.ta-stat-icon {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: rgba(75, 86, 148, 0.11);
    color: #4B5694;
    font-size: 1.12rem;
}
.ta-stat-value {
    color: #063B00;
    font-size: 1.22rem;
    font-weight: 850;
    line-height: 1.05;
}
.ta-stat-label {
    color: #64748b;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0;
    text-transform: uppercase;
    margin-top: 4px;
}
.ta-subject-side {
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-radius: 16px;
    background: #F8FAFC;
    border: 1px solid rgba(75, 86, 148, 0.12);
    padding: 16px;
}
.ta-instructor {
    display: grid;
    grid-template-columns: 40px minmax(0, 1fr);
    gap: 11px;
    align-items: center;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(15, 23, 42, 0.08);
}
.ta-avatar {
    display: grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border-radius: 13px;
    background: #4B5694;
    color: #ffffff;
    font-weight: 850;
}
.ta-side-label {
    color: #64748b;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
}
.ta-side-value {
    color: #101828;
    font-size: 0.92rem;
    font-weight: 800;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.ta-meta-list {
    display: grid;
    gap: 9px;
}
.ta-meta-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    color: #64748b;
    font-size: 0.8rem;
}
.ta-meta-row strong {
    color: #334155;
    font-weight: 800;
}
.ta-status-pill {
    color: #166534;
    background: #DCFCE7;
    border-radius: 999px;
    padding: 3px 8px;
    font-size: 0.72rem;
    font-weight: 850;
}
@media (max-width: 760px) {
    .ta-subject-card {
        padding: 18px;
    }
    .ta-subject-grid {
        grid-template-columns: 1fr;
    }
    .ta-subject-side {
        padding: 14px;
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
            f'<div class="ta-stat-icon">{_safe(icon)}</div>'
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
        '<div class="ta-subject-kicker">&#128218; Subject</div>'
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
