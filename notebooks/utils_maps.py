import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_zlewnia_stat(
    zlewnie_gdf,
    woj_gdf,
    stats_df,
    stat_column,
    title,
    cmap='Blues',
    cbar_label=None
):
    """
    Rysuje mapę zlewni z pokolorowaną warstwą statystyki, etykietami ID i kolorbarem.

    Parametry:
    - zlewnie_gdf: GeoDataFrame z geometrią zlewni (musi mieć kolumnę 'Zlewnia ID')
    - woj_gdf: GeoDataFrame z województwami
    - stats_df: DataFrame z kolumnami 'Zlewnia ID' i wartością statystyki
    - stat_column: str, kolumna z wartością do wizualizacji
    - title: str, tytuł wykresu
    - cmap: str, kolormap (np. 'Blues', 'viridis')
    - cbar_label: str, etykieta dla kolorbaru
    """

    # Połączenie statystyk z geometrią
    merged = zlewnie_gdf.merge(stats_df, on='Zlewnia ID', how='left')

    # Rysowanie mapy
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    woj_gdf.plot(ax=ax, color="#f7f7f7", edgecolor="black", linewidth=0.8)

    # Główna warstwa zlewni
    merged.plot(
        ax=ax,
        column=stat_column,
        cmap=cmap,
        edgecolor="green",
        linewidth=0.8,
        legend=False  # wyłącz domyślny legend
    )

    # Etykiety zlewni (ID)
    for _, row in merged.iterrows():
        if row['geometry'] is not None and not row['geometry'].is_empty:
            centroid = row['geometry'].centroid
            ax.text(
                centroid.x, centroid.y,
                str(row['Zlewnia ID']),
                fontsize=8,
                ha='center', va='center',
                color='black'
            )

    # Dodanie kolorbara z kontrolą
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # Skalowanie kolorów
    vmin = merged[stat_column].min()
    vmax = merged[stat_column].max()
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []  # wymagane dla plt.colorbar

    cb = plt.colorbar(sm, cax=cax, orientation="vertical")
    cb.ax.set_position([
        cb.ax.get_position().x0,
        cb.ax.get_position().y0 + 0.1,  # podnieś
        cb.ax.get_position().width,
        cb.ax.get_position().height * 0.8  # skróć
    ])

    if cbar_label:
        cb.set_label(cbar_label, fontsize=12)

    # Opis osi i tytuł
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Longtitude [m]", fontsize=12)
    ax.set_ylabel("Latitude [m]", fontsize=12)
    ax.tick_params(labelsize=10)
    plt.tight_layout()
    plt.show()
