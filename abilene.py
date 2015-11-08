"""Custom Abilene topology

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=abilene' from the command line.
"""

from mininet.topo import Topo

class Abilene( Topo ):
    "Abilene topology."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        hSTTLng = self.addHost( 'h1' )
        sSTTLng = self.addSwitch( 's1' )

        hSNVAng = self.addHost( 'h2' )
        sSNVAng = self.addSwitch( 's2' )

        hDNVRng = self.addHost( 'h3' )
        sDNVRng = self.addSwitch( 's3' )

        hLOSAng = self.addHost( 'h4' )
        sLOSAng = self.addSwitch( 's4' )

        hKSCYng = self.addHost( 'h5' )
        sKSCYng = self.addSwitch( 's5' )

        hHSTNng = self.addHost( 'h6' )
        sHSTNng = self.addSwitch( 's6' )

        hATLAng = self.addHost( 'h7' )
        sATLAng = self.addSwitch( 's7' )

        hATLA_M5 = self.addHost( 'h8' )
        sATLA_M5 = self.addSwitch( 's8' )

        hIPLSng = self.addHost( 'h9' )
        sIPLSng = self.addSwitch( 's9' )

        hCHINng = self.addHost( 'h10' )
        sCHINng = self.addSwitch( 's10' )

        hNYCMng = self.addHost( 'h11' )
        sNYCMng = self.addSwitch( 's11' )

        hWASHng = self.addHost( 'h12' )
        sWASHng = self.addSwitch( 's12' )

        # Add links
        self.addLink( hSTTLng, sSTTLng )
        self.addLink( hSNVAng, sSNVAng )
        self.addLink( hDNVRng, sDNVRng )
        self.addLink( hLOSAng, sLOSAng )
        self.addLink( hKSCYng, sKSCYng )
        self.addLink( hHSTNng, sHSTNng )
        self.addLink( hATLAng, sATLAng )
        self.addLink( hATLA_M5, sATLA_M5 )
        self.addLink( hIPLSng, sIPLSng )
        self.addLink( hCHINng, sCHINng )
        self.addLink( hNYCMng, sNYCMng )
        self.addLink( hWASHng, sWASHng )

        self.addLink( sSTTLng, sSNVAng )
        self.addLink( sSTTLng, sDNVRng )
        self.addLink( sSNVAng, sDNVRng )
        self.addLink( sSNVAng, sLOSAng )
        self.addLink( sLOSAng, sHSTNng )
        self.addLink( sKSCYng, sHSTNng )
        self.addLink( sDNVRng, sKSCYng )
        self.addLink( sKSCYng, sIPLSng )
        self.addLink( sHSTNng, sATLAng )
        self.addLink( sATLAng, sIPLSng )
        self.addLink( sIPLSng, sCHINng )
        self.addLink( sCHINng, sNYCMng )
        self.addLink( sATLAng, sATLA_M5 )
        self.addLink( sATLAng, sWASHng )
        self.addLink( sWASHng, sNYCMng )

topos = { 'abilene': ( lambda: Abilene() ) }
