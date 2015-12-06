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
        hATLA_M5 = self.addHost( 'h1' )
        sATLA_M5 = self.addSwitch( 's1' )

        hATLAng = self.addHost( 'h2' )
        sATLAng = self.addSwitch( 's2' )

        hCHINng = self.addHost( 'h3' )
        sCHINng = self.addSwitch( 's3' )

        hDNVRng = self.addHost( 'h4' )
        sDNVRng = self.addSwitch( 's4' )

        hHSTNng = self.addHost( 'h5' )
        sHSTNng = self.addSwitch( 's5' )

        hIPLSng = self.addHost( 'h6' )
        sIPLSng = self.addSwitch( 's6' )

        hKSCYng = self.addHost( 'h7' )
        sKSCYng = self.addSwitch( 's7' )

        hLOSAng = self.addHost( 'h8' )
        sLOSAng = self.addSwitch( 's8' )

        hNYCMng = self.addHost( 'h9' )
        sNYCMng = self.addSwitch( 's9' )

        hSNVAng = self.addHost( 'h10' )
        sSNVAng = self.addSwitch( 's10' )

        hSTTLng = self.addHost( 'h11' )
        sSTTLng = self.addSwitch( 's11' )

        hWASHng = self.addHost( 'h12' )
        sWASHng = self.addSwitch( 's12' )

        # Add links
        self.addLink( hATLA_M5, sATLA_M5 )
        self.addLink( hATLAng, sATLAng )
        self.addLink( hCHINng, sCHINng )
        self.addLink( hDNVRng, sDNVRng )
        self.addLink( hHSTNng, sHSTNng )
        self.addLink( hIPLSng, sIPLSng )
        self.addLink( hKSCYng, sKSCYng )
        self.addLink( hLOSAng, sLOSAng )
        self.addLink( hNYCMng, sNYCMng )
        self.addLink( hSNVAng, sSNVAng )
        self.addLink( hSTTLng, sSTTLng )
        self.addLink( hWASHng, sWASHng )        


        self.addLink( sATLA_M5, sATLAng )

        self.addLink( sATLAng, sHSTNng )
        self.addLink( sATLAng, sIPLSng )
        self.addLink( sATLAng, sWASHng )

        self.addLink( sCHINng, sIPLSng )
        self.addLink( sCHINng, sNYCMng )

        self.addLink( sDNVRng, sKSCYng )
        self.addLink( sDNVRng, sSNVAng )
        self.addLink( sDNVRng, sSTTLng )

        self.addLink( sHSTNng, sKSCYng )
        self.addLink( sHSTNng, sLOSAng )

        self.addLink( sIPLSng, sKSCYng )
        
        self.addLink( sLOSAng, sSNVAng )

        self.addLink( sNYCMng, sWASHng )

        self.addLink( sSNVAng, sSTTLng )

topos = { 'abilene': ( lambda: Abilene() ) }
