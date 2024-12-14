import typer


@app.command()
def calculate_friis(
    pt_dbm: float = typer.Argument(..., help="Transmitter power in dBm"),
    gt_db: float = typer.Argument(..., help="Transmitter antenna gain in dB"),
    gr_db: float = typer.Argument(..., help="Receiver antenna gain in dB"),
    f_mhz: float = typer.Argument(..., help="Frequency in MHz"),
    d_km: float = typer.Argument(..., help="Distance in kilometers"),
) -> None:
    """
    Calculate the received power using Friis' Transmission Formula
    """
    import math

    c = data["constants"]["c"]
    f_hz = f_mhz * 1e6
    wavelength = c / f_hz
    d_m = d_km * 1e3

    pr_dbm = pt_dbm + gt_db + gr_db + 20 * math.log10(wavelength / (4 * math.pi * d_m))

    typer.echo(f"Received Power (Pr): {pr_dbm:.2f} dBm")


@app.command()
def smith_chart(file: str = typer.Argument(..., help="Path to s-parameter file")):
    """
    Plot the SMith Chart from an s-parameter file
    """
    import numpy as np
    import skrf as rf
    import termplotlib as tpl

    # Load or create a network
    network = rf.Network(frequency=rf.Frequency(1, 10, 101, "ghz"), s=[[0.5 + 0.5j]])

    # Extract data for polar plotting
    magnitudes = np.abs(network.s[:, 0, 0])
    phases = np.angle(network.s[:, 0, 0])

    # Convert to degrees for terminal display
    phases_deg = np.degrees(phases)

    # Create a polar plot
    fig = tpl.figure()
    fig.plot(phases_deg, magnitudes, plot_type="polar", width=60, height=20)
    fig.show()
